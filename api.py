"""
Vendor Invoice Intelligence — API Layer
========================================
Thin FastAPI service that sits between the new web frontend and the
existing, unmodified ML inference functions:

    inference.predict_freight.predict_freight_cost
    inference.predict_invoice_flag.predict_invoice_flag

No model training logic, feature definitions, preprocessing, or scaler
usage has been changed. This file only validates incoming requests,
calls the existing functions, and shapes the response as JSON.

Run from the project root (so the relative "models/..." paths used by
the inference modules resolve correctly):

    uvicorn api:app --reload --port 8000
"""

import pathlib

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from inference.predict_freight import predict_freight_cost
from inference.predict_invoice_flag import predict_invoice_flag

app = FastAPI(
    title="Vendor Invoice Intelligence API",
    description="Serves the existing freight-cost and invoice-flagging models.",
    version="1.0.0",
)

# The frontend is a static HTML/CSS/JS bundle that may be opened from a
# different origin (e.g. a local dev server or file host), so CORS is
# opened for the API routes only. Nothing else on the backend is exposed.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# ----------------------------------------------------------------------
# Request / response schemas
# ----------------------------------------------------------------------
class FreightRequest(BaseModel):
    quantity: float = Field(..., gt=0, description="Total units on the purchase order")
    dollars: float = Field(..., gt=0, description="Total invoice value in USD")


class FreightResponse(BaseModel):
    predicted_freight: float


class InvoiceRequest(BaseModel):
    invoice_quantity: float = Field(..., gt=0)
    invoice_dollars: float = Field(..., gt=0)
    freight: float = Field(..., ge=0)
    days_po_to_invoice: float = Field(..., ge=0)
    total_item_quantity: float = Field(..., gt=0)
    total_item_dollars: float = Field(..., gt=0)
    avg_receiving_delay: float = Field(..., ge=0)


class InvoiceResponse(BaseModel):
    status: str
    confidence: float
    flag_probability: float


# ----------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------
@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/predict/freight", response_model=FreightResponse)
def predict_freight(payload: FreightRequest):
    try:
        input_data = {
            "Quantity": [payload.quantity],
            "Dollars": [payload.dollars],
        }
        result = predict_freight_cost(input_data)
        predicted = float(result["Predicted_Freight"].iloc[0])
    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="Freight model artifact not found on the server (models/predict_freight_model.pkl).",
        )
    except Exception as exc:  # keep the frontend contract intact on unexpected failures
        raise HTTPException(status_code=500, detail=f"Freight prediction failed: {exc}")

    return {"predicted_freight": round(predicted, 2)}


@app.post("/api/predict/invoice", response_model=InvoiceResponse)
def predict_invoice(payload: InvoiceRequest):
    try:
        # Field order/names mirror the exact keys inference/predict_invoice_flag.py expects.
        input_data = {
            "invoice_quantity": [payload.invoice_quantity],
            "invoice_dollars": [payload.invoice_dollars],
            "Freight": [payload.freight],
            "days_po_to_invoice": [payload.days_po_to_invoice],
            "total_item_quantity": [payload.total_item_quantity],
            "total_item_dollars": [payload.total_item_dollars],
            "avg_receiving_delay": [payload.avg_receiving_delay],
        }
        result = predict_invoice_flag(input_data)
        status = str(result["Predicted_Status"].iloc[0])
        confidence = float(result["Confidence (%)"].iloc[0])
        flag_probability = float(result["Flagged Probability (%)"].iloc[0])
    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="Invoice model or scaler artifact not found on the server (models/).",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Invoice prediction failed: {exc}")

    return {
        "status": status,
        "confidence": confidence,
        "flag_probability": flag_probability,
    }


# ----------------------------------------------------------------------
# Static frontend (served AFTER API routes so /api/* takes priority)
# ----------------------------------------------------------------------
_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent


@app.get("/")
def serve_index():
    """Serve the main frontend page."""
    return FileResponse(_PROJECT_ROOT / "index.html")


# Mount static assets (CSS, JS) — the "html=False" default keeps this
# from interfering with the API routes defined above.
app.mount("/", StaticFiles(directory=str(_PROJECT_ROOT)), name="static")

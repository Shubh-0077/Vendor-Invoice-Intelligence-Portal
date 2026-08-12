# Vendor Invoice Intelligence Portal

AI-powered platform for freight cost prediction and vendor invoice risk assessment, built for finance and accounts payable teams.

🚀 **[Live Demo](https://vendor-invoice-intelligence-portal-1.onrender.com/)**  

🔌 [API](https://vendor-invoice-intelligence-portal-j9ac.onrender.com) ([health check](https://vendor-invoice-intelligence-portal-j9ac.onrender.com/api/health))

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

<p align="center">
  <img src="assets/screenshots/banner.png" alt="Vendor Invoice Intelligence Portal banner" width="100%">
</p>

<p align="center"><em>📷 Project banner. Insert a wide (1280×640) banner image at <code>assets/screenshots/banner.png</code></em></p>

---

## 📖 Overview

This is a machine-learning-powered finance operations app with two modules:

- **Freight Cost Prediction**: estimates expected freight cost from purchase order quantity and invoice value.
- **Invoice Risk Assessment**: evaluates a vendor invoice and flags it as safe for automatic processing or a candidate for manual review.

The frontend is a lightweight HTML/CSS/JS interface that calls a FastAPI backend, which runs inference through trained scikit-learn models.

---

## 🖼️ Application Preview

### 🏠 Overview
> <img width="1619" height="905" alt="Screenshot 2026-08-11 225204" src="https://github.com/user-attachments/assets/94a1e386-21c8-4764-8e8c-df1bdb4a637f" />


### 🚚 Freight Cost Prediction
> <img width="1919" height="909" alt="Screenshot 2026-08-11 225245" src="https://github.com/user-attachments/assets/d819e6c9-b957-4ed7-a4c9-8bf8e9e54b20" />


### 🚨 Invoice Risk Assessment
> <img width="1902" height="906" alt="Screenshot 2026-08-11 225432" src="https://github.com/user-attachments/assets/61c1d8e5-5f95-420e-a5f6-6b27d4d56612" />


---

## ✨ Key Features

- Freight cost prediction (regression)
- Invoice risk assessment (classification)
- Real-time ML inference via REST API
- FastAPI backend with a documented health endpoint
- Custom HTML/CSS/JavaScript frontend
- Confidence score and risk level shown per prediction
- Cloud-deployed frontend and backend

---

## 🖱️ How to Use the Live Application

1. Open the [Live Demo](https://vendor-invoice-intelligence-portal-1.onrender.com/).
2. Choose **Freight Cost Prediction** or **Invoice Risk Assessment** from the sidebar.
3. Enter the requested invoice/purchase order values.
4. Submit the form.
5. View the prediction, along with confidence and (for risk assessment) a risk level indicator.

---

## 🧰 Technology Stack

**Frontend** -> 
HTML · CSS · JavaScript

**Backend** -> 
Python · FastAPI · Uvicorn

**Machine Learning** -> 
scikit-learn · pandas · NumPy

**Data** -> 
SQLite

**Deployment** -> 
Render

---

## 🔄 How It Works

```
User
 ↓
HTML / CSS / JavaScript
 ↓
FastAPI REST API
 ↓
ML Inference (scikit-learn)
 ↓
Trained Models (.pkl)
 ↓
Prediction
 ↓
Frontend Result
```

---

## 📂 Project Structure

```
├── api.py                    # FastAPI backend, serves predictions
├── index.html                # Frontend UI
├── script.js                 # Frontend logic, calls the API
├── style.css
├── freight_cost_prediction/  # Freight regression training pipeline
├── invoice_flagging/         # Invoice risk classification training pipeline
├── inference/                # Inference wrappers used by the API
├── models/                   # Serialized models (.pkl)
├── notebooks/                # EDA and experimentation
├── requirements.txt
└── README.md
```

---

## 🤖 Machine Learning

**Freight Cost Prediction**
- Problem type: Regression
- Inputs: Quantity, Invoice Dollars
- Model: Linear Regression
- Result: R² ≈ 0.95 on held-out test data

**Invoice Risk Assessment**
- Problem type: Binary classification (Approved / Flagged for Manual Review)
- Inputs: Invoice quantity, invoice dollars, freight, total item quantity, total item dollars, PO-to-invoice days, average receiving delay
- Model: Random Forest, tuned with RandomizedSearchCV
- Result: ~99% accuracy on held-out test data

> **Limitation:** The invoice risk classifier is trained on self-defined rule-based labels, not historical audited outcomes. Its output should be treated as a triage signal for manual review, not a validated fraud or error prediction.

---

## 🔌 API

| Endpoint | Description |
|---|---|
| `GET /api/health` | Health check, returns `{"status":"ok"}` |
| `POST /api/predict/freight` | Returns predicted freight cost |
| `POST /api/predict/invoice` | Returns invoice risk prediction with confidence and probability |

---

## ⚙️ Run Locally

```bash
git clone https://github.com/Shubh-0077/Vendor-Invoice-Intelligence-Portal.git
cd Vendor-Invoice-Intelligence-Portal

pip install -r requirements.txt

uvicorn api:app --reload --port 8000
```

The API will run at `http://localhost:8000`. Open `index.html` in a browser to use the frontend, and update the API base URL in `script.js` to `http://localhost:8000` so it points at your local backend.

---

## ☁️ Deployment

- Frontend deployed as a static site on Render.
- Backend deployed as a FastAPI web service on Render.
- Frontend calls the backend over REST; all ML inference runs server-side.

---

## 📈 Business Impact

| Area | Impact |
|---|---|
| **Operational Efficiency** | Routine, low-risk invoices move through faster without full manual review. |
| **Reduced Manual Review** | Reviewer attention is concentrated on the ~35% of invoices flagged as higher risk. |
| **Decision Support** | Confidence scores and a risk level indicator give reviewers a quantified starting point. |
| **Cost Optimization** | Freight predictions offer a consistent baseline for spotting overcharges. |
| **Time Savings** | Real-time inference replaces slower, manual, invoice-by-invoice checks. |

> Figures above reflect model performance on the evaluation dataset; real-world impact should be validated with production monitoring.

---

## 🧠 Skills Demonstrated

| Category | Skills |
|---|---|
| Programming | Python, SQL, JavaScript |
| Machine Learning | Regression, classification, ensemble methods, hyperparameter tuning |
| Statistics | Descriptive statistics, correlation analysis, class distribution analysis |
| Feature Engineering | Business-rule label design, SQL aggregation, derived date features |
| EDA & Visualization | Matplotlib, Seaborn, Plotly |
| API Development | FastAPI, REST API design, Uvicorn |
| Frontend Development | HTML, CSS, JavaScript |
| Deployment | Cloud deployment on Render, frontend/backend service separation |
| Version Control | Git, GitHub |
| Business Analytics | Translating a finance problem into a measurable ML solution |
| Problem Solving | Root-causing and fixing a production train/inference scaling bug |

---
## ⚠️ Limitations

The invoice risk model's labels are self-defined business rules rather than confirmed audit outcomes, so predictions should support manual review, not replace it.

---
## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

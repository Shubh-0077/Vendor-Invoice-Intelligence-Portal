import streamlit as st
import pandas as pd

from inference.predict_freight import predict_freight_cost
from inference.predict_invoice_flag import predict_invoice_flag

# ==========================================================
# Page Configuration
# ==========================================================
st.set_page_config(
    page_title="Vendor Invoice Intelligence Portal",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# Styling — ADDITIVE ONLY.
# ----------------------------------------------------------
# Rules followed here on purpose, after earlier breakage:
#   1. Never set `visibility: hidden` or `display: none` on
#      any Streamlit chrome (header/toolbar/menu) — that's
#      what hid the Deploy button before.
#   2. Never override `.stApp` / body background — theme text
#      colors are tuned to the actual background Streamlit
#      picks, so overriding one without the other is what made
#      the title unreadable before.
#   3. Never target internal radio/checkbox DOM structure —
#      that's what broke the sidebar selector before.
#   4. Every selector below only ADDS a font, a color accent,
#      or spacing to elements that already render by default.
#      If a selector doesn't match in your Streamlit version,
#      the element just falls back to normal styling — nothing
#      disappears or throws an error.
#   5. No structural HTML (no hand-built <div> cards). All
#      layout uses real Streamlit containers, which always
#      wrap their children correctly.
# ==========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=IBM+Plex+Mono:wght@500;600&display=swap');

    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
    }

    .eyebrow {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.75rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #14B8A6;
        font-weight: 600;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        opacity: 0.75;
        font-size: 0.98rem;
        max-width: 700px;
        line-height: 1.5;
    }

    [data-testid="stMetricValue"] {
        font-family: 'IBM Plex Mono', monospace;
    }
    [data-testid="stMetricLabel"] {
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.75rem;
        opacity: 0.7;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# Small helper — just picks an emoji + label for the gauge,
# no HTML, no styling risk.
# ==========================================================
def risk_label(pct: float) -> str:
    if pct < 30:
        return "🟢 Low risk"
    elif pct < 60:
        return "🟡 Medium risk"
    return "🔴 High risk"


# ==========================================================
# Sidebar
# ==========================================================
with st.sidebar:
    st.title("🧾 Invoice Intelligence")
    st.caption("Finance ML Platform")

    selected_model = st.radio(
        "Prediction Module",
        (
            "Freight Cost Prediction",
            "Invoice Manual Approval Flag",
        ),
    )

    st.divider()

    with st.container(border=True):
        st.markdown("**Business Benefits**")
        st.markdown(
            """
            - 📉 Better freight forecasting
            - 🧾 Detect risky invoices early
            - ⚡ Reduce manual review load
            - 💰 Lower financial leakage
            """
        )

    st.divider()
    st.caption("Built with Scikit-learn · Random Forest · SQLite · Joblib · Streamlit")

# ==========================================================
# Header
# ==========================================================
st.markdown('<div class="eyebrow">Finance · Machine Learning</div>', unsafe_allow_html=True)
st.title("Vendor Invoice Intelligence Portal")
st.markdown(
    '<div class="subtitle">Two production ML models supporting the finance team: '
    "freight cost estimation ahead of invoice approval, and automated triage of vendor "
    "invoices that warrant manual review.</div>",
    unsafe_allow_html=True,
)

st.write("")
chip_col1, chip_col2, chip_col3, chip_col4 = st.columns(4)
chip_col1.metric("Active Models", "2")
chip_col2.metric("Algorithm", "Random Forest")
chip_col3.metric("Inference", "Real-Time")
chip_col4.metric("Data Source", "SQLite")

st.divider()

# ==========================================================
# Module 1 — Freight Cost Prediction
# ==========================================================
if selected_model == "Freight Cost Prediction":

    with st.container(border=True):
        st.subheader("🚚 Freight Cost Prediction")
        st.write(
            "Estimate expected freight cost from invoice quantity and dollar value, "
            "for budgeting and vendor negotiation ahead of invoice approval."
        )

        with st.form("freight_form"):
            col1, col2 = st.columns(2)

            with col1:
                quantity = st.number_input(
                    "Quantity",
                    min_value=1,
                    value=1200,
                    help="Total units on the purchase order.",
                )

            with col2:
                dollars = st.number_input(
                    "Invoice Dollars",
                    min_value=1.0,
                    value=18500.0,
                    help="Total invoice value in USD.",
                )

            submit = st.form_submit_button("Predict Freight Cost", use_container_width=True)

    if submit:
        # ---- ML inference call (unchanged) ----
        input_data = {
            "Quantity": [quantity],
            "Dollars": [dollars],
        }
        result = predict_freight_cost(input_data)
        predicted_freight = result["Predicted_Freight"].iloc[0]

        st.write("")
        st.success("Prediction completed successfully.")

        with st.container(border=True):
            res_col1, res_col2, res_col3 = st.columns(3)
            res_col1.metric("Estimated Freight Cost", f"${predicted_freight:,.2f}")
            res_col2.metric("Input Quantity", f"{quantity:,}")
            res_col3.metric("Invoice Value", f"${dollars:,.2f}")

        with st.expander("View raw model output"):
            st.dataframe(result, use_container_width=True)

# ==========================================================
# Module 2 — Invoice Manual Approval Flagging
# ==========================================================
else:

    with st.container(border=True):
        st.subheader("🚨 Invoice Manual Approval Prediction")
        st.write(
            "Classify a vendor invoice as safe for automatic approval or as a candidate "
            "for manual review, based on cost, freight, and delivery-timing signals."
        )

        with st.form("invoice_form"):
            col1, col2 = st.columns(2)

            with col1:
                invoice_quantity = st.number_input("Invoice Quantity", min_value=1, value=100)
                invoice_dollars = st.number_input("Invoice Dollars", min_value=1.0, value=5000.0)
                freight = st.number_input("Freight", min_value=0.0, value=120.0)
                days_po_to_invoice = st.number_input("PO to Invoice Days", min_value=0, value=3)

            with col2:
                total_item_quantity = st.number_input("Total Item Quantity", min_value=1, value=100)
                total_item_dollars = st.number_input("Total Item Dollars", min_value=1.0, value=4998.0)
                avg_receiving_delay = st.number_input("Average Receiving Delay", min_value=0.0, value=4.0)

            submit = st.form_submit_button("Evaluate Invoice", use_container_width=True)

    if submit:
        # ---- ML inference call (unchanged) ----
        input_data = {
            "invoice_quantity": [invoice_quantity],
            "invoice_dollars": [invoice_dollars],
            "Freight": [freight],
            "days_po_to_invoice": [days_po_to_invoice],
            "total_item_quantity": [total_item_quantity],
            "total_item_dollars": [total_item_dollars],
            "avg_receiving_delay": [avg_receiving_delay],
        }

        result = predict_invoice_flag(input_data)

        status = result["Predicted_Status"].iloc[0]
        confidence = result["Confidence (%)"].iloc[0]
        probability = result["Flagged Probability (%)"].iloc[0]

        st.write("")
        with st.container(border=True):
            st.subheader("Prediction Result")

            if status == "Approved":
                st.success("✅ Approved — safe for automatic processing")
            else:
                st.error("🚨 Flagged for manual review")

            res_col1, res_col2 = st.columns(2)
            res_col1.metric("Model Confidence", f"{confidence:.2f}%")
            res_col2.metric("Flag Probability", f"{probability:.2f}%")

            st.caption(f"Risk gauge — {risk_label(probability)}")
            st.progress(min(100, max(0, int(round(probability)))) / 100)

            with st.expander("View input summary & raw model output"):
                st.dataframe(result, use_container_width=True)

# ==========================================================
# Footer
# ==========================================================
st.divider()
foot_col1, foot_col2 = st.columns(2)
foot_col1.caption("Vendor Invoice Intelligence Portal · Internal Finance Tooling")
foot_col2.caption("Python · Scikit-learn · SQLite · Streamlit")
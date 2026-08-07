<div align="center">

# 🧾 Vendor Invoice Intelligence Portal

### AI-Driven Freight Cost Prediction & Automated Invoice Risk Flagging for Finance Operations

Two production-grade machine learning models, deployed in a real-time Streamlit app, that predict freight costs and automatically triage vendor invoices for manual review.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Scikit--Learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-Compute-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Viz-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)

[**Live Demo**](#-demo) · [**Screenshots**](#-application-preview) · [**Installation**](#-installation) · [**Report a Bug**](https://github.com/USERNAME/REPO/issues)

</div>

<br>

<div align="center">

📷 **Project Banner**
*(Insert project banner image here)*

</div>

<br>

---

## 📖 Overview

**Vendor Invoice Intelligence Portal** is an end-to-end machine learning application built for finance and accounts-payable teams who process high volumes of vendor invoices every month.

It solves two problems that are traditionally manual, slow, and inconsistent:

- **How much should this invoice's freight cost be?** — answered by a regression model trained on historical purchase data.
- **Does this invoice need a human to look at it?** — answered by a classifier trained on invoice, purchase order, and receiving signals, using business-rule-engineered risk labels.

Both models are served in real time through a Streamlit application, giving finance analysts an instant, data-driven second opinion on every invoice — without replacing human judgment on the invoices that matter most.

> **Why it matters:** Reviewing every invoice with equal effort wastes time on low-risk transactions and risks missing the handful that need real scrutiny. This project routes attention where it's actually needed.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🚚 **Freight Cost Prediction** | Regression model estimates expected freight cost from quantity and invoice value. |
| 🚨 **Invoice Risk Detection** | Classifier flags invoices likely to need manual review, based on 7 engineered features. |
| ⚡ **Real-Time Predictions** | Sub-second inference through a live Streamlit interface — no batch jobs required. |
| 📊 **Interactive Dashboard** | Clean, two-module Streamlit UI built for non-technical finance users. |
| 🎯 **Confidence Scoring** | Every classification includes a model confidence percentage. |
| 🌡️ **Risk Probability & Gauge** | Visual, intuitive read on how risky a flagged invoice actually is. |
| 🔌 **Production Inference Pipeline** | Modular, reusable inference scripts decoupled from the UI layer. |
| 🧮 **Business Rule Engine** | Transparent, auditable risk-scoring logic behind the ML label — not a black box. |
| 🌲 **Tuned Random Forest** | Hyperparameter-optimized via `RandomizedSearchCV` with 5-fold cross-validation. |
| 🗄️ **SQLite Integration** | Direct SQL extraction and feature aggregation from a relational invoice database. |

---

## 💼 Business Problem

Organizations processing thousands of vendor invoices per month face recurring, costly friction:

- ❌ Manual invoice verification, invoice by invoice
- ❌ Inconsistent, ad hoc freight cost estimation
- ❌ Slow, bottlenecked approval cycles
- ❌ Financial leakage from invoices that should have been caught but weren't
- ❌ Human error at high review volume
- ❌ Delayed vendor payments

Accounts payable automation is one of the most practical, high-ROI applications of machine learning in finance — the data is structured, the decisions are repeatable, and the cost of a missed anomaly is measurable. Left unaddressed, these challenges scale linearly (or worse) with invoice volume, while manual review capacity doesn't.

---

## 🛠️ Solution

The portal applies two independent ML models to the invoice lifecycle, giving finance teams a consistent, explainable decision layer in place of ad hoc manual judgment.

```
                     Vendor Invoice
                           │
                           ▼
                  ┌──────────────────┐
                  │  Data Validation │
                  └──────────────────┘
                           │
                           ▼
                  ┌───────────────────┐
                  │Feature Engineering│
                  └───────────────────┘
                           │
                           ▼
                  ┌───────────────────┐
                  │    ML Models      │
                  │───────────────────│
                  │ Freight Regressor │
                  │ Risk Classifier   │
                  └───────────────────┘
                           │
                           ▼
                  ┌───────────────────┐
                  │    Prediction     │
                  │ Cost · Status ·   │
                  │ Confidence · Risk │
                  └───────────────────┘
                           │
                           ▼
                  ┌───────────────────┐
                  │ Business Decision │
                  │ Approve / Review  │
                  └───────────────────┘
```

---

## 🖼️ Application Preview

<div align="center">

| | |
|---|---|
| 📷 **Home Page** <br> *(Insert: Streamlit landing screen)* | 📷 **Freight Prediction Screen** <br> *(Insert: Freight input form)* |
| 📷 **Freight Prediction Result** <br> *(Insert: Predicted freight cost output)* | 📷 **Invoice Flagging Screen** <br> *(Insert: Invoice input form)* |
| 📷 **Invoice Prediction Result** <br> *(Insert: Approved/Flagged output)* | 📷 **Risk Gauge** <br> *(Insert: Risk gauge visualization)* |
| 📷 **Model Performance** <br> *(Insert: Confusion matrix / metrics view)* | 📷 **Architecture Diagram** <br> *(Insert: System architecture diagram)* |
| 📷 **Repository Structure** <br> *(Insert: Folder tree screenshot)* | |

</div>

---

## 🎬 Demo

| Resource | Link |
|---|---|
| ☁️ Streamlit Cloud | `[Insert Streamlit Cloud URL]` |


---

## 🏗️ Project Architecture

<div align="center">

📷 **Architecture Diagram**
*(Insert: Full system architecture diagram)*

</div>

```
┌─────────────────────────────────────────────────────────────┐
│                        DATA LAYER                           │
│   SQLite (inventory.db)  →  purchases + vendor_invoice      │
└───────────────────────────────┬─────────────────────────────┘
                                 │  SQL extraction & aggregation
                                 ▼
┌──────────────────────────────────────────────────────────────┐
│                     TRAINING PIPELINE                        │
│  Feature Engineering → Business-Rule Labeling → Preprocessing│
│  → Model Training → Hyperparameter Tuning → Evaluation       │
└───────────────────────────────┬──────────────────────────────┘
                                 │  Joblib serialization
                                 ▼
┌─────────────────────────────────────────────────────────────┐
│                      MODEL ARTIFACTS                        │
│  predict_freight_model.pkl · predict_flag_invoice.pkl       │
│  scaler.pkl                                                 │
└───────────────────────────────┬─────────────────────────────┘
                                 │  loaded at inference time
                                 ▼
┌─────────────────────────────────────────────────────────────┐
│                    INFERENCE + UI LAYER                     │
│  predict_freight.py · predict_invoice_flag.py  →  app.py    │
│                    (Streamlit Application)                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧰 Tech Stack

| Category | Technologies |
|---|---|
| **Programming Language** | Python 3.10+ |
| **Machine Learning** | Scikit-learn (Random Forest, Linear Regression, RandomizedSearchCV) |
| **Data Manipulation** | Pandas, NumPy |
| **Database** | SQLite |
| **Visualization** | Matplotlib, Seaborn, Plotly |
| **Deployment** | Streamlit |
| **Model Persistence** | Joblib |
| **Development Tools** | Jupyter Notebook, VS Code |
| **Version Control** | Git, GitHub |

---

## 🔄 Machine Learning Pipeline

```
Business Understanding
        │
        ▼
   Data Collection  (SQL extraction from inventory.db)
        │
        ▼
        EDA  (distributions, correlations, risk conditions)
        │
        ▼
 Feature Engineering  (aggregations, date deltas, risk score)
        │
        ▼
   Preprocessing  (train/test split, StandardScaler)
        │
        ▼
   Model Training  (Decision Tree → Random Forest)
        │
        ▼
Hyperparameter Tuning  (RandomizedSearchCV, 5-fold CV)
        │
        ▼
     Evaluation  (accuracy, F1, confusion matrix)
        │
        ▼
      Inference  (predict_freight.py / predict_invoice_flag.py)
        │
        ▼
     Deployment  (Streamlit application)
```

---

## 🤖 Models Used

| Model | Purpose | Performance | Final Selection |
|---|---|---|---|
| Linear Regression | Freight cost estimation | R² ≈ 0.95 · MAE ≈ 27 · RMSE ≈ 174 | ✅ Selected |
| Decision Tree Regressor | Freight cost benchmark | Lower generalization than linear baseline | ❌ |
| Random Forest Regressor | Freight cost benchmark | Comparable, added complexity without a clear gain | ❌ |
| Decision Tree Classifier | Invoice risk benchmark | Higher variance, overfits | ❌ |
| Random Forest Classifier | Invoice risk benchmark | ~99% accuracy, untuned | ❌ |
| **Random Forest + RandomizedSearchCV** | Invoice risk classification | **98.9% accuracy** | ✅ **Selected** |

**Why these models won:**
- **Linear Regression** matched tree-based alternatives on accuracy while staying fully interpretable — an easy sell to non-technical finance stakeholders.
- **Tuned Random Forest** delivered the same raw accuracy as the untuned version but with cross-validated hyperparameters, giving it better expected generalization to unseen invoices.

<details>
<summary><strong>📌 Best Hyperparameters (click to expand)</strong></summary>

```python
{
    "n_estimators": 300,
    "max_depth": None,
    "min_samples_split": 5,
    "min_samples_leaf": 1,
    "max_features": "log2"
}
```

</details>

---

## 📊 Model Performance

### Classification — Invoice Flagging

| Class | Precision | Recall | F1-Score |
|---|---|---|---|
| 0 — Approved | 0.98 | 1.00 | 0.99 |
| 1 — Flagged | 1.00 | 0.97 | 0.98 |

**Overall Accuracy: 98.9%**

<details>
<summary><strong>📌 Confusion Matrix (click to expand)</strong></summary>

**Before Hyperparameter Tuning**

|  | Predicted: Approved | Predicted: Flagged |
|---|---|---|
| **Actual: Approved** | 721 | 12 |
| **Actual: Flagged** | 0 | 376 |

**After Hyperparameter Tuning**

|  | Predicted: Approved | Predicted: Flagged |
|---|---|---|
| **Actual: Approved** | 721 | 13 |
| **Actual: Flagged** | 0 | 375 |

</details>

### Regression — Freight Cost Prediction

| Metric | Value |
|---|---|
| MAE | ≈ 27 |
| RMSE | ≈ 174 |
| R² | ≈ 0.95 |

<div align="center">

📷 **Confusion Matrix**
*(Insert: Confusion matrix visualization)*

📷 **Feature Importance**
*(Insert: Feature importance chart)*

📷 **Model Comparison**
*(Insert: Model comparison chart)*

</div>

---

## 📂 Folder Structure

```
Vendor-Invoice-Intelligence/
│
├── app.py                          # Streamlit application entry point
│
├── models/                         # Serialized model artifacts (Joblib)
│   ├── predict_freight_model.pkl
│   ├── predict_flag_invoice.pkl
│   └── scaler.pkl
│
├── inference/                      # Production inference wrappers
│   ├── predict_freight.py
│   └── predict_invoice_flag.py
│
├── invoice_flagging/                # Training pipeline
│   ├── train.py
│   ├── model_eval.py
│   └── data_preprocessing.py
│
├── notebooks/                      # Exploratory & experimental notebooks
│   ├── Freight Prediction.ipynb
│   └── Invoice Flagging.ipynb
│
├── data/
│   └── inventory.db                # SQLite source database
│
├── requirements.txt                # Python dependencies
└── README.md
```

| Path | Purpose |
|---|---|
| `app.py` | User-facing Streamlit app — wires both modules together. |
| `models/` | Trained regression/classification models and the fitted scaler. |
| `inference/` | Loads a model + scaler and returns predictions for new input. |
| `invoice_flagging/` | End-to-end training pipeline: data prep, training, evaluation. |
| `notebooks/` | EDA and experimentation for each module. |
| `data/` | Source SQLite database. |

---

## ⚙️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/USERNAME/REPO.git
cd REPO

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Streamlit app
streamlit run app.py
```

The app will be available at `http://localhost:8501`.

---

## 🚀 Usage

### 🚚 Freight Cost Prediction

1. Open the app and select **Freight Cost Prediction** from the sidebar.
2. Enter **Quantity** and **Invoice Dollars**.
3. Click **Predict Freight Cost**.
4. View the **Estimated Freight Cost** returned instantly.

### 🚨 Invoice Manual Approval Flagging

1. Select **Invoice Manual Approval Flag** from the sidebar.
2. Enter the seven invoice/PO features (quantity, dollars, freight, timing, and receiving signals).
3. Click **Evaluate Invoice**.
4. Review the output:
   - **Predicted Status** — `Approved` or `Flagged for Manual Review`
   - **Confidence Score** — model's certainty in the prediction
   - **Flag Probability** — likelihood the invoice needs review
   - **Risk Gauge** — quick visual read on invoice risk

---

## 📈 Business Impact

| Area | Impact |
|---|---|
| **Operational Efficiency** | Routine, low-risk invoices move through faster without full manual review. |
| **Reduced Manual Review** | Reviewer attention is concentrated on the ~35% of invoices flagged as higher risk. |
| **Decision Support** | Confidence scores and a risk gauge give reviewers a quantified starting point. |
| **Cost Optimization** | Freight predictions offer a consistent baseline for spotting overcharges. |
| **Time Savings** | Real-time inference replaces slower, manual, invoice-by-invoice checks. |

> Figures above reflect model performance on the evaluation dataset; real-world impact should be validated with production monitoring.

---

## 🧠 Skills Demonstrated

| Category | Skills |
|---|---|
| Programming | Python, SQL |
| Machine Learning | Regression, classification, ensemble methods, hyperparameter tuning |
| Statistics | Descriptive statistics, correlation analysis, class distribution analysis |
| Feature Engineering | Business-rule label design, SQL aggregation, derived date features |
| EDA & Visualization | Matplotlib, Seaborn, Plotly |
| Deployment | Streamlit application development |
| Version Control | Git, GitHub |
| Business Analytics | Translating a finance problem into a measurable ML solution |
| Problem Solving | Root-causing and fixing a production train/inference scaling bug |

---

## 📄 License

This project is licensed under the `[Insert License, e.g., MIT]` License — see the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Shubh-0077)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](http://www.linkedin.com/in/shubhammalkar)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://shubhammalkar.framer.website/)
[![Email](https://img.shields.io/badge/Email-Contact-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:codewleo@gmail.com)

</div>

<div align="center">

⭐ If you found this project useful, consider giving it a star!

</div>

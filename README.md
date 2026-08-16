<div align="center">

# Vendor Invoice Intelligence Portal

**AI-powered platform for freight cost prediction and vendor invoice risk assessment, built for finance and accounts payable teams.**

<br>

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Random Forest](https://img.shields.io/badge/Random%20Forest-ML-6B7280?style=flat-square)
![Linear Regression](https://img.shields.io/badge/Linear%20Regression-ML-6B7280?style=flat-square)

</div>

<p align="center">
  <img width="100%" height="887" alt="image" src="https://github.com/user-attachments/assets/a2c71200-ea88-4f71-b354-a6d5603bc8ea" />
</p>

---
| 🚀 Live Demo | 🔌 API |
|---|---|
| [Open Application](https://vendor-invoice-intelligence-portal-1.onrender.com/) | [API Endpoint](https://vendor-invoice-intelligence-portal-j9ac.onrender.com) · [Health Check](https://vendor-invoice-intelligence-portal-j9ac.onrender.com/api/health) |

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
INVOICE-INTELLIGENCE/
│
├── freight_cost_prediction/      # Freight cost regression training pipeline
│   ├── data_preprocessing.py     # Feature engineering & data preparation
│   ├── model_evaluation.py       # Metrics & evaluation scripts
│   └── train.py                  # Model training pipeline
│
├── invoice_flagging/             # Invoice risk classification training pipeline
│   ├── data_preprocessing.py     # Feature engineering & data preparation
│   ├── model_eval.py             # Metrics & evaluation scripts
│   └── train.py                  # Model training pipeline
│
├── inference/                    # Inference wrappers for real-time predictions
│   ├── __init__.py               # Package initializer
│   ├── predict_freight.py        # Inference pipeline for freight prediction
│   └── predict_invoice_flag.py   # Inference pipeline for invoice flagging
│
├── models/                       # Serialized trained models & preprocessors
│   ├── predict_flag_invoice.pkl  # Classification model artifact
│   ├── predict_freight_model.pkl # Regression model artifact
│   └── scaler.pkl                # Feature scaler
│
├── notebooks/                    # EDA and experimental notebooks
│   ├── Invoice Flagging.ipynb
│   └── Predicting Freight Cost .ipynb
│
├── api.py                        # FastAPI backend serving prediction endpoints
├── app.py                        # Application entry point / server script
├── index.html                    # Frontend user interface
├── script.js                     # Frontend logic & API call handling
├── style.css                     # Custom styling for UI
├── requirements.txt              # Project dependencies
└── README.md                     # Project documentation
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

---
## 📬 Contact

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Shubh-0077)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](http://www.linkedin.com/in/shubhammalkar)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://shubhammalkar.framer.website/)
[![Email](https://img.shields.io/badge/Email-Contact-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:codewleo@gmail.com)

</div>

<div align="center"> ⭐ If you found this project useful, consider giving it a star!! </div>

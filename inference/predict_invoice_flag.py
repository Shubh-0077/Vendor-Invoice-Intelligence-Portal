import joblib
import pandas as pd

MODEL_PATH = "models/predict_flag_invoice.pkl"
SCALER_PATH = "models/scaler.pkl"


def load_model(model_path: str = MODEL_PATH):
    """
    Load the trained Invoice Flagging model.
    """
    with open(model_path, "rb") as f:
        model = joblib.load(f)
    return model


def load_scaler(scaler_path: str = SCALER_PATH):
    """
    Load the fitted StandardScaler.
    """
    with open(scaler_path, "rb") as f:
        scaler = joblib.load(f)
    return scaler


def predict_invoice_flag(input_data):
    """
    Predict whether a vendor invoice should be flagged for manual review.

    Parameters
    ----------
    input_data : dict
        Dictionary containing invoice features.

    Returns
    -------
    pd.DataFrame
        Input data along with prediction, confidence score,
        and probability of being flagged.
    """

    model = load_model()
    scaler = load_scaler()

    # Convert input to DataFrame
    input_df = pd.DataFrame(input_data)

    # Scale input using the SAME scaler used during training
    input_scaled = scaler.transform(input_df)

    # Predictions
    predictions = model.predict(input_scaled)
    probabilities = model.predict_proba(input_scaled)

    # Confidence = highest probability
    confidence = probabilities.max(axis=1)

    # Output dataframe
    result_df = input_df.copy()

    result_df["Predicted_Status"] = [
        "Flagged for Manual Review" if pred == 1 else "Approved"
        for pred in predictions
    ]

    result_df["Confidence (%)"] = (confidence * 100).round(2)

    result_df["Flagged Probability (%)"] = (
        probabilities[:, 1] * 100
    ).round(2)

    return result_df


if __name__ == "__main__":

    # Example inference run (Local Testing)
    sample_data = {
        "invoice_quantity": [100, 600, 250],
        "invoice_dollars": [5000, 25000, 12000],
        "Freight": [120, 350, 180],
        "days_po_to_invoice": [3, 7, 4],
        "total_item_quantity": [100, 610, 250],
        "total_item_dollars": [4998, 24800, 11990],
        "avg_receiving_delay": [4, 15, 6]
    }

    prediction = predict_invoice_flag(sample_data)
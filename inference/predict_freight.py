import joblib 
import pandas as pd 

MODEL_PATH = "models/predict_freight_model.pkl"

def load_model(model_path: str = MODEL_PATH):
    """
    Load trained Freight prediction model
    """
    with open(model_path,"rb") as f:
        model = joblib.load(f)
    return model

def predict_freight_cost(input_data):
    """
    Predict Freight Cost for new vendor invoices

    Parameters
    -----------
    input_data : dict 

    Returns
    -----------
    pd.DataFrame with predicted freight cost    
    """
    model = load_model()
    input_df = pd.DataFrame(input_data)
    input_df['Predicted_Freight'] = model.predict(input_df).round()
    return input_df 

if __name__ == "__main__": 

    # example inference run(local testing)
    sample_data = {
    "Quantity": [25, 75, 150, 400, 800],
    "Dollars": [600, 1800, 4500, 12000, 25000]
    }

    prediction = predict_freight_cost(sample_data)
    print(prediction)
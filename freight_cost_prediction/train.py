import joblib 
from pathlib import Path

from data_preprocessing import load_vendor_df, prepare_feature, split_data 
from model_evaluation import train_lr, train_dt, train_rf, model_eval   

def main():
    BASE_DIR = Path(__file__).resolve().parent
    db_path = BASE_DIR.parent / "data" / "inventory.db"

    model_dir = BASE_DIR / "models"
    model_dir.mkdir(exist_ok=True)

    print("Database Path:", db_path)
    print("Database Exists:", db_path.exists())

    # Load data
    df = load_vendor_df(db_path)

    # Prepare data 
    x,y = prepare_feature(df)
    x_train, x_test, y_train, y_test = split_data(x,y)

    # Train Models
    lr_model = train_lr(x_train,y_train)
    dt_model = train_dt(x_train,y_train)
    rf_model = train_rf(x_train,y_train) 

    # Evaluate Models 
    results = []
    results.append(model_eval(lr_model, x_test, y_test, "Linear Regression"))
    results.append(model_eval(dt_model, x_test, y_test, "Decision Tree Regressor"))
    results.append(model_eval(rf_model, x_test, y_test, "Random Forest Regressor"))

    # Select BEST model (Lowest MAE)
    best_model_info = min(results, key=lambda x:x['mae'])
    best_model_name = best_model_info["model_name"]

    best_model = {
        'Linear Regression' : lr_model,
        'Decision Tree Regressor' : dt_model,
        'Random Forest Regressor' : rf_model        
    }[best_model_name]

    # Save BEST Model  
    model_path = model_dir/"predict_freight_model.pkl"
    joblib.dump(best_model,model_path)  

    print(f"\n BEST model saved: {best_model_name}")
    print(f"Model path : {model_path}") 


if __name__ == "__main__": 
    main()
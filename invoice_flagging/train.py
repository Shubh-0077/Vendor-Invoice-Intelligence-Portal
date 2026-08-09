from model_eval import train_random_forest, eval_classifier
from data_preprocessing import (load_invoice_data, apply_labels, split_data, scale_features) 
import joblib 

FEATURES = ['invoice_quantity',
        'invoice_dollars',
        'Freight',
        'days_po_to_invoice',
        'total_item_quantity',
        'total_item_dollars',
        'avg_receiving_delay']

TARGET = "flag_invoice"


def main():

    # load data 
    df = load_invoice_data()
    df = apply_labels(df) 

    # Prepare data 
    x_train, x_test, y_train, y_test = split_data(df,FEATURES,TARGET)
    x_train_scaled, x_test_scaled = scale_features(x_train,x_test, 'models/scaler.pkl')

    # Train & eval model 
    random_search = train_random_forest(x_train, y_train)

    eval_classifier(
        random_search.best_estimator_,
        x_test,
        y_test,
        "Random Forest Classifier"
        )

    # Save the best model 
    joblib.dump(random_search.best_estimator_,'models/predict_flag_invoice.pkl') 

if __name__ == "__main__":
    main()



    
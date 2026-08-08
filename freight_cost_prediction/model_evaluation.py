import numpy as np

from sklearn.linear_model import LinearRegression 
from sklearn.tree import DecisionTreeRegressor 
from sklearn.ensemble import RandomForestRegressor 

from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score

def train_lr(x_train,y_train):
    model = LinearRegression()
    model.fit(x_train,y_train)
    return model 

def train_dt(x_train,y_train,max_depth=5):
    model = DecisionTreeRegressor(
        max_depth = max_depth ,random_state=42
    )
    model.fit(x_train,y_train)
    return model 

def train_rf(x_train,y_train,max_depth=5):
    model = RandomForestRegressor(
        max_depth = max_depth ,random_state=42
    )
    model.fit(x_train,y_train)
    return model 

def model_eval(model,x_test,y_test, model_name :str) -> dict: 
    """
    Evaluate Models and return mertics
    """
    y_pred = model.predict(x_test)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred) * 100

    print(f"\n{model_name} Performance:")
    print(f"MAE : {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R² Score: {r2:.4f}")

    return{
        "model_name" : model_name,
        "mae" : mae,
        "rmse" : rmse,
        "r2" : r2
    }
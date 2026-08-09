import numpy as np 
import pandas as pd 
import joblib  
import sqlite3 

from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler  


def load_invoice_data():
    conn = sqlite3.connect('D:/PROJETS/Invoice Intelligence/data/inventory.db') 

    # Lets merge these two tables and creat a final df for our project

    query =  """ 
            WITH purchases_agg as ( 
                SELECT 
                    p.PONumber,
                    COUNT(DISTINCT p.Brand) as total_brands,
                    SUM(p.Quantity) as total_item_quantity,
                    SUM(p.Dollars) as total_item_dollars,
                    avg(julianday(p.ReceivingDate) - julianday(p.PODate)) as avg_receiving_delay 
                FROM purchases p
                GROUP BY p.PONumber
            )
            
            SELECT 
                vi.PONumber, 
                vi.Quantity as invoice_quantity, 
                vi.Dollars as invoice_dollars,
                vi.Freight, 
                (julianday(vi.InvoiceDate) - julianday(vi.PODate)) as days_po_to_invoice,
                (julianday(vi.PayDate) - julianday(vi.InvoiceDate)) as days_to_pay, 
                pa.total_brands, 
                pa.total_item_quantity, 
                pa.total_item_dollars, 
                pa.avg_receiving_delay
                
            FROM vendor_invoice vi
            LEFT JOIN purchases_agg pa
                ON vi.PONumber = pa.PONumber
            """ 

    df = pd.read_sql_query(query,conn)
    conn.close()
    return df  



def create_invoice_risk_label(row):

    risk_score = 0

    if abs(row["invoice_dollars"] - row["total_item_dollars"]) > 5:
        risk_score += 1

    if row["avg_receiving_delay"] > 10:
        risk_score += 1

    if row["Freight"] > 200:
        risk_score += 1

    if row["invoice_quantity"] > 500:
        risk_score += 1

    return 1 if risk_score >= 2 else 0 

def apply_labels(df): 
    df["flag_invoice"] = df.apply(create_invoice_risk_label, axis=1)  
    return df 


def split_data(df,features,target): 
    x = df[features]
    y = df[target] 

    return train_test_split(
        x,y,test_size=0.2,random_state=42
    )

def scale_features(x_train,x_test,scaler_path): 
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    joblib.dump(scaler,'models/scaler.pkl')
    return x_train_scaled, x_test_scaled
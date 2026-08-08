import sqlite3
import pandas as pd 
from sklearn.model_selection import train_test_split 

def load_vendor_df(db_path: str):
    """
    Load Vendor Invoice Data from SQLite Database 
    """
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM vendor_invoice"
    df = pd.read_sql_query(query,conn)
    conn.close()
    return df 

def prepare_feature(df: pd.DataFrame): 
    """
    Select features & target columns 
    """
    x = df[['Quantity','Dollars']]
    y = df['Freight']
    return x,y  

def split_data(x,y, test_size = 0.2 ,random_state = 42): 
    """
    Split dataset into train & test sets
    """
    return train_test_split(
        x,
        y,
        test_size =test_size ,
        random_state = random_state
    )
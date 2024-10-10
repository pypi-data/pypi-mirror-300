import pandas as pd

def get_data_summary(df: pd.DataFrame):
    return {
        'Missing Values': df.isnull().sum(),
        'Data Types': df.dtypes,
        'Shape': df.shape,
        'Basic Stats': df.describe(),
    }

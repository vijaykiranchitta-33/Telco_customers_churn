import pandas as pd

def engineer_features(df):
    df = df.copy()
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
    services = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
    df['Total_Services'] = (df[services] == 'Yes').sum(axis=1)
    df['Avg_Monthly_Cost'] = df['TotalCharges'] / df['tenure'].replace(0, 1)
    df['Monthly_Diff'] = df['MonthlyCharges'] - df['Avg_Monthly_Cost']
    df['Has_Protection'] = ((df['OnlineSecurity'] == 'Yes') | (df['OnlineBackup'] == 'Yes')).astype(int)
    return df
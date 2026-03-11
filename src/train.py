import pandas as pd
import joblib
import xgboost as xgb
import os
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.model_selection import train_test_split
from preprocessing import engineer_features

def train():
    df = pd.read_csv('data/telco_churn.csv')
    df = engineer_features(df)
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
    
    X_raw = df.drop(['customerID', 'Churn'], axis=1)
    X = pd.get_dummies(X_raw, drop_first=True)
    y = df['Churn']
    
    if not os.path.exists('models'): os.makedirs('models')
    joblib.dump(X.columns.tolist(), 'models/model_columns.joblib')
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    rf = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
    xgb_mod = xgb.XGBClassifier(n_estimators=150, learning_rate=0.05, max_depth=5, random_state=42)
    
    model = VotingClassifier(estimators=[('rf', rf), ('xgb', xgb_mod)], voting='soft')
    model.fit(X_train, y_train)
    
    joblib.dump(model, 'models/voting_model.joblib')
    print(f"Model trained! Test Accuracy: {model.score(X_test, y_test):.4f}")

if __name__ == "__main__":
    train()
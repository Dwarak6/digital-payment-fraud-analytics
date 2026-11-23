"""
Fraud Risk Scoring & Machine Learning Analysis
Trains a risk prediction model and evaluates business cost-benefit trade-offs.
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, precision_recall_curve, confusion_matrix

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACT_PATH = os.path.join(PROJECT_DIR, "data", "processed", "powerbi_fact_transactions.csv")
MERCH_PATH = os.path.join(PROJECT_DIR, "data", "processed", "powerbi_dim_merchants.csv")
CUST_PATH = os.path.join(PROJECT_DIR, "data", "processed", "powerbi_dim_customers.csv")

def run_ml_pipeline():
    print("Loading data for ML Pipeline...")
    df_tx = pd.read_csv(FACT_PATH)
    df_merch = pd.read_csv(MERCH_PATH)
    df_cust = pd.read_csv(CUST_PATH)
    
    # Merge dimensions for feature engineering
    df = df_tx.merge(df_merch[["MerchantID", "MerchantCategory", "RiskTier"]], on="MerchantID", how="left")
    df = df.merge(df_cust[["CustomerID", "CustomerSegment", "KYCStatus", "CreditScoreTier"]], on="CustomerID", how="left")
    
    # Select feature columns
    features = [
        "Amount", "TransactionHour", "PaymentMethod", "DeviceType",
        "IPCountry", "IsVPNorProxy", "MerchantCategory", "KYCStatus", "CreditScoreTier"
    ]
    
    X = df[features].copy()
    y = df["IsFraud"]
    
    # One-hot encode categorical features
    X = pd.get_dummies(X, drop_first=True)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    
    print(f"Training RandomForestClassifier on {len(X_train)} samples with {X_train.shape[1]} features...")
    clf = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1, class_weight='balanced')
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]
    
    roc_auc = roc_auc_score(y_test, y_prob)
    cm = confusion_matrix(y_test, y_pred)
    
    print("\n--- Model Performance Evaluation ---")
    print(f"ROC-AUC Score: {roc_auc:.4f}")
    print("\nConfusion Matrix:")
    print(cm)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, digits=4))
    
    # Feature Importances
    importances = pd.Series(clf.feature_importances_, index=X.columns).sort_values(ascending=False).head(10)
    print("\nTop 10 Fraud Predictor Features:")
    print(importances)
    
    # Calculate Business Impact (Cost of False Positives vs Loss Prevented)
    # Assume 1 False Positive costs INR 150 (customer support + customer friction friction loss)
    # True Positive saves the transaction amount
    test_indices = y_test.index
    test_amounts = df.loc[test_indices, "Amount"]
    
    tp_mask = (y_test == 1) & (y_pred == 1)
    fp_mask = (y_test == 0) & (y_pred == 1)
    fn_mask = (y_test == 1) & (y_pred == 0)
    
    saved_loss = test_amounts[tp_mask].sum()
    missed_loss = test_amounts[fn_mask].sum()
    fp_friction_cost = fp_mask.sum() * 150
    net_savings = saved_loss - fp_friction_cost
    
    print("\n--- Financial Impact & ROI ---")
    print(f"Fraud Loss Prevented by Model: INR {saved_loss:,.2f}")
    print(f"Missed Fraud Loss (False Negatives): INR {missed_loss:,.2f}")
    print(f"Customer Friction Cost (False Positives): INR {fp_friction_cost:,.2f}")
    print(f"Net Financial Benefit: INR {net_savings:,.2f}")
    
    return clf, X.columns, importances

if __name__ == "__main__":
    run_ml_pipeline()

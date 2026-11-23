"""
Digital Payment & Fraud Analytics - Synthetic Data Generator
Generates realistic fintech transactions, customer demographics, merchant profiles, and date dimension.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set seeds for reproducibility
np.random.seed(42)
random.seed(42)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(PROJECT_DIR, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(PROJECT_DIR, "data", "processed")

os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

NUM_CUSTOMERS = 3000
NUM_MERCHANTS = 150
NUM_TRANSACTIONS = 45000
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 12, 31)

def generate_customers():
    print("Generating Customers dimension...")
    segments = ["Retail Consumer", "Affluent / HNI", "Student", "SME Business", "Gig Economy Worker"]
    segment_weights = [0.45, 0.15, 0.15, 0.15, 0.10]
    
    kyc_levels = ["Full KYC", "Minimum KYC", "e-KYC Pending"]
    kyc_weights = [0.75, 0.20, 0.05]
    
    credit_tiers = ["Tier 1 (750+)", "Tier 2 (650-749)", "Tier 3 (550-649)", "Tier 4 (<550)"]
    credit_weights = [0.40, 0.35, 0.18, 0.07]
    
    locations = [
        ("Mumbai", "Maharashtra", "West"),
        ("Bengaluru", "Karnataka", "South"),
        ("Delhi NCR", "Delhi", "North"),
        ("Hyderabad", "Telangana", "South"),
        ("Chennai", "Tamil Nadu", "South"),
        ("Pune", "Maharashtra", "West"),
        ("Kolkata", "West Bengal", "East"),
        ("Ahmedabad", "Gujarat", "West"),
        ("Jaipur", "Rajasthan", "North"),
        ("Lucknow", "Uttar Pradesh", "North"),
    ]
    
    customers = []
    for cid in range(1001, 1001 + NUM_CUSTOMERS):
        city, state, region = random.choice(locations)
        signup_offset = random.randint(0, 365 * 3) # Up to 3 years ago
        signup_date = (START_DATE - timedelta(days=signup_offset)).strftime("%Y-%m-%d")
        
        segment = np.random.choice(segments, p=segment_weights)
        kyc = np.random.choice(kyc_levels, p=kyc_weights)
        credit = np.random.choice(credit_tiers, p=credit_weights)
        
        # Risk propensity based on KYC & credit
        risk_base = 0.02
        if kyc == "e-KYC Pending":
            risk_base += 0.15
        elif kyc == "Minimum KYC":
            risk_base += 0.05
        if credit == "Tier 4 (<550)":
            risk_base += 0.10
            
        customers.append({
            "CustomerID": f"CUST-{cid:05d}",
            "CustomerSegment": segment,
            "City": city,
            "State": state,
            "Region": region,
            "Age": random.randint(19, 68),
            "SignupDate": signup_date,
            "KYCStatus": kyc,
            "CreditScoreTier": credit,
            "AccountRiskWeight": round(risk_base, 3)
        })
        
    df = pd.DataFrame(customers)
    df.to_csv(os.path.join(RAW_DATA_DIR, "customers.csv"), index=False)
    df.to_csv(os.path.join(PROCESSED_DATA_DIR, "powerbi_dim_customers.csv"), index=False)
    return df

def generate_merchants():
    print("Generating Merchants dimension...")
    categories = [
        ("E-Commerce Retail", "Low", 0.015),
        ("Digital Goods & Gaming", "High", 0.065),
        ("Travel & Airlines", "Medium", 0.035),
        ("Cryptocurrency Exchange", "Critical", 0.110),
        ("Electronics & Gadgets", "Medium-High", 0.050),
        ("Food & Grocery", "Low", 0.008),
        ("Healthcare & Pharmacy", "Low", 0.005),
        ("Luxury & Jewelry", "High", 0.070),
        ("Subscription Services", "Medium", 0.025),
        ("Financial & Lending", "Medium-High", 0.045)
    ]
    
    merchants = []
    for mid in range(5001, 5001 + NUM_MERCHANTS):
        cat_info = random.choice(categories)
        cat_name, risk_tier, base_fraud_rate = cat_info
        
        merchant_name = f"{cat_name.split()[0]}-{random.choice(['Hub', 'Pay', 'Mart', 'Zone', 'Direct', 'Express', 'Global', 'Prime'])}-{mid%100:02d}"
        
        merchants.append({
            "MerchantID": f"MERCH-{mid:04d}",
            "MerchantName": merchant_name,
            "MerchantCategory": cat_name,
            "RiskTier": risk_tier,
            "BaseFraudRate": base_fraud_rate,
            "SettlementPeriodDays": random.choice([1, 2, 3, 7]),
            "ChargebackThresholdPct": 1.0  # Industry standard 1.0% chargeback breach limit
        })
        
    df = pd.DataFrame(merchants)
    df.to_csv(os.path.join(RAW_DATA_DIR, "merchants.csv"), index=False)
    df.to_csv(os.path.join(PROCESSED_DATA_DIR, "powerbi_dim_merchants.csv"), index=False)
    return df

def generate_date_dimension():
    print("Generating Date dimension...")
    dates = []
    curr = START_DATE
    while curr <= END_DATE:
        dates.append({
            "Date": curr.strftime("%Y-%m-%d"),
            "Year": curr.year,
            "Quarter": f"Q{((curr.month - 1) // 3) + 1}",
            "YearQuarter": f"{curr.year}-Q{((curr.month - 1) // 3) + 1}",
            "Month": curr.month,
            "MonthName": curr.strftime("%B"),
            "YearMonth": curr.strftime("%Y-%m"),
            "Day": curr.day,
            "DayOfWeek": curr.strftime("%A"),
            "DayOfWeekNumber": curr.weekday() + 1,
            "IsWeekend": 1 if curr.weekday() >= 5 else 0
        })
        curr += timedelta(days=1)
        
    df = pd.DataFrame(dates)
    df.to_csv(os.path.join(RAW_DATA_DIR, "dim_date.csv"), index=False)
    df.to_csv(os.path.join(PROCESSED_DATA_DIR, "powerbi_dim_date.csv"), index=False)
    return df

def generate_transactions(cust_df, merch_df):
    print("Generating Fact Transactions...")
    
    payment_methods = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Digital Wallet"]
    pay_weights = [0.42, 0.28, 0.15, 0.08, 0.07]
    
    device_types = ["Android Mobile", "iOS Mobile", "Windows Desktop", "MacOS Desktop", "Tablet"]
    device_weights = [0.55, 0.25, 0.12, 0.05, 0.03]
    
    cust_dict = cust_df.set_index("CustomerID").to_dict(orient="index")
    merch_dict = merch_df.set_index("MerchantID").to_dict(orient="index")
    
    cust_ids = cust_df["CustomerID"].values
    merch_ids = merch_df["MerchantID"].values
    
    total_days = (END_DATE - START_DATE).days
    
    transactions = []
    
    # We will simulate ~45,000 transactions over 2025
    for tid in range(1, NUM_TRANSACTIONS + 1):
        # Pick customer & merchant
        cid = np.random.choice(cust_ids)
        mid = np.random.choice(merch_ids)
        
        c_meta = cust_dict[cid]
        m_meta = merch_dict[mid]
        
        # Pick timestamp
        day_offset = random.randint(0, total_days)
        hour = random.choices(
            population=list(range(24)),
            weights=[1.5, 1.0, 0.8, 0.5, 0.4, 0.8, 2.0, 3.5, 5.0, 6.5, 7.5, 7.0, 6.5, 6.0, 5.5, 6.0, 7.0, 8.5, 8.0, 7.0, 5.5, 4.0, 2.5, 1.8]
        )[0]
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        tx_time = START_DATE + timedelta(days=day_offset, hours=hour, minutes=minute, seconds=second)
        
        pay_method = np.random.choice(payment_methods, p=pay_weights)
        device = np.random.choice(device_types, p=device_weights)
        
        # IP Country & Proxy flags
        is_foreign_ip = np.random.choice([0, 1], p=[0.94, 0.06])
        ip_country = "India" if is_foreign_ip == 0 else random.choice(["USA", "UK", "Russia", "Nigeria", "Singapore", "Netherlands"])
        is_vpn_or_proxy = np.random.choice([0, 1], p=[0.96, 0.04]) if is_foreign_ip == 0 else np.random.choice([0, 1], p=[0.5, 0.5])
        
        # Amount calculation by category
        cat = m_meta["MerchantCategory"]
        if cat in ["Cryptocurrency Exchange", "Luxury & Jewelry"]:
            base_amt = np.random.exponential(scale=35000) + 5000
        elif cat in ["Travel & Airlines", "Electronics & Gadgets"]:
            base_amt = np.random.exponential(scale=18000) + 2000
        elif cat in ["Food & Grocery", "Healthcare & Pharmacy"]:
            base_amt = np.random.exponential(scale=1200) + 150
        else:
            base_amt = np.random.exponential(scale=4500) + 300
            
        base_amt = round(min(max(base_amt, 50), 450000), 2)
        
        # Fraud probability logic
        fraud_prob = m_meta["BaseFraudRate"] + c_meta["AccountRiskWeight"]
        
        # Night hour bonus
        if hour in [0, 1, 2, 3, 4]:
            fraud_prob *= 2.2
        # Foreign IP / VPN bonus
        if is_foreign_ip == 1:
            fraud_prob *= 3.0
        if is_vpn_or_proxy == 1:
            fraud_prob *= 2.5
        # High value bonus
        if base_amt > 80000:
            fraud_prob *= 2.0
            
        # Payment method risk variation
        if pay_method == "Credit Card":
            fraud_prob *= 1.3
        elif pay_method == "Digital Wallet":
            fraud_prob *= 1.1
        elif pay_method == "UPI":
            fraud_prob *= 0.8
            
        fraud_prob = min(fraud_prob, 0.85)
        is_fraud = 1 if (random.random() < fraud_prob) else 0
        
        # If fraud, assign fraud pattern type
        fraud_type = "None"
        chargeback_status = "No Dispute"
        if is_fraud == 1:
            fraud_type = random.choices(
                ["Card Testing", "Account Takeover", "Friendly Fraud", "Stolen Identity", "Velocity Abuse"],
                weights=[0.28, 0.32, 0.15, 0.15, 0.10]
            )[0]
            # High chance of dispute/chargeback
            chargeback_status = random.choices(
                ["Chargeback Initiated", "Chargeback Won", "Chargeback Lost", "Under Dispute Review"],
                weights=[0.25, 0.15, 0.45, 0.15]
            )[0]
            
        # Simulated Risk Score (0 - 100)
        # Fraudulent transactions have right-skewed risk scores
        if is_fraud == 1:
            risk_score = round(min(np.random.normal(loc=82, scale=11), 99.9), 1)
        else:
            risk_score = round(max(np.random.normal(loc=24, scale=16), 1.0), 1)
            
        # Transaction Status (Success, Flagged & Blocked, Failed / Bank Decline)
        if risk_score >= 88.0:
            tx_status = "Blocked by Rule Engine"
            status_flag = "Blocked"
        elif is_fraud == 1 and risk_score < 88.0:
            tx_status = "Completed (Fraud Undetected)"
            status_flag = "Completed"
        else:
            tx_status = np.random.choice(["Completed", "Bank Declined", "User Cancelled"], p=[0.92, 0.05, 0.03])
            status_flag = "Completed" if tx_status == "Completed" else "Declined"

        # Financial impact calculations
        fraud_loss_amount = base_amt if (is_fraud == 1 and status_flag == "Completed") else 0.0
        prevented_loss_amount = base_amt if (is_fraud == 1 and status_flag == "Blocked") else 0.0

        transactions.append({
            "TransactionID": f"TXN-{tid:08d}",
            "TransactionTimestamp": tx_time.strftime("%Y-%m-%d %H:%M:%S"),
            "TransactionDate": tx_time.strftime("%Y-%m-%d"),
            "TransactionHour": hour,
            "CustomerID": cid,
            "MerchantID": mid,
            "PaymentMethod": pay_method,
            "DeviceType": device,
            "IPCountry": ip_country,
            "IsVPNorProxy": is_vpn_or_proxy,
            "Amount": base_amt,
            "TransactionStatus": tx_status,
            "IsStatusCompleted": 1 if status_flag == "Completed" else 0,
            "RiskScore": risk_score,
            "RiskBand": "Low (0-30)" if risk_score < 30 else ("Medium (30-69)" if risk_score < 70 else "High (70-100)"),
            "IsFraud": is_fraud,
            "FraudType": fraud_type,
            "ChargebackStatus": chargeback_status,
            "FraudLossAmount": round(fraud_loss_amount, 2),
            "PreventedLossAmount": round(prevented_loss_amount, 2)
        })
        
    df = pd.DataFrame(transactions)
    df.to_csv(os.path.join(RAW_DATA_DIR, "transactions.csv"), index=False)
    df.to_csv(os.path.join(PROCESSED_DATA_DIR, "powerbi_fact_transactions.csv"), index=False)
    
    print(f"Dataset generated successfully! Total transactions: {len(df)}")
    print(f"Overall Fraud Count: {df['IsFraud'].sum()} ({df['IsFraud'].mean()*100:.2f}%)")
    print(f"Total Completed Fraud Loss: INR {df['FraudLossAmount'].sum():,.2f}")
    print(f"Total Blocked Fraud Loss Prevented: INR {df['PreventedLossAmount'].sum():,.2f}")
    return df

if __name__ == "__main__":
    cust_df = generate_customers()
    merch_df = generate_merchants()
    date_df = generate_date_dimension()
    tx_df = generate_transactions(cust_df, merch_df)
    print("All datasets generated & saved to data/raw and data/processed.")

-- ====================================================================
-- PROJECT: FinGuard - Digital Payment Fraud Analytics
-- SCRIPT: 03_risk_segmentation_queries.sql
-- DESCRIPTION: Merchant Risk Profiling, Chargeback Ratio Violations, and KYC Impact
-- ====================================================================

-- 1. Identify High-Risk Merchants Breaching the 1.0% Regulatory Chargeback Threshold
WITH MerchantMetrics AS (
    SELECT 
        m.MerchantID,
        m.MerchantName,
        m.MerchantCategory,
        m.RiskTier,
        COUNT(t.TransactionID) AS Total_Transactions,
        ROUND(SUM(t.Amount), 2) AS Total_GMV,
        COUNT(CASE WHEN t.ChargebackStatus LIKE '%Chargeback%' THEN 1 END) AS Chargeback_Count,
        SUM(t.IsFraud) AS Fraud_Count,
        ROUND(SUM(t.FraudLossAmount), 2) AS Total_Fraud_Loss
    FROM dim_merchant m
    JOIN fact_transactions t ON m.MerchantID = t.MerchantID
    GROUP BY m.MerchantID, m.MerchantName, m.MerchantCategory, m.RiskTier
)
SELECT 
    MerchantID,
    MerchantName,
    MerchantCategory,
    RiskTier,
    Total_Transactions,
    Total_GMV,
    Chargeback_Count,
    ROUND((Chargeback_Count * 100.0 / NULLIF(Total_Transactions, 0)), 2) AS Chargeback_Rate_Pct,
    Total_Fraud_Loss,
    CASE 
        WHEN (Chargeback_Count * 100.0 / NULLIF(Total_Transactions, 0)) >= 1.0 THEN 'CRITICAL: Breached Card Scheme Threshold (Hold Escrow)'
        WHEN (Chargeback_Count * 100.0 / NULLIF(Total_Transactions, 0)) >= 0.75 THEN 'WARNING: High Chargeback Watchlist'
        ELSE 'HEALTHY'
    END AS Merchant_Compliance_Status
FROM MerchantMetrics
ORDER BY Chargeback_Rate_Pct DESC, Total_Fraud_Loss DESC;

-- 2. KYC Status & Credit Score Vulnerability Analysis
SELECT 
    c.KYCStatus,
    c.CreditScoreTier,
    COUNT(DISTINCT c.CustomerID) AS Customer_Count,
    COUNT(t.TransactionID) AS Transaction_Volume,
    SUM(t.IsFraud) AS Total_Fraud_Incidents,
    ROUND(AVG(t.IsFraud) * 100, 2) AS Fraud_Rate_Pct,
    ROUND(SUM(t.FraudLossAmount), 2) AS Total_Fraud_Loss_INR,
    ROUND(AVG(t.RiskScore), 1) AS Avg_Customer_Risk_Score
FROM dim_customer c
JOIN fact_transactions t ON c.CustomerID = t.CustomerID
GROUP BY c.KYCStatus, c.CreditScoreTier
ORDER BY Total_Fraud_Loss_INR DESC;

-- 3. Geographic & Cross-Border Anomaly Breakdown
SELECT 
    t.IPCountry,
    t.IsVPNorProxy,
    COUNT(t.TransactionID) AS Total_Txs,
    SUM(t.IsFraud) AS Fraud_Txs,
    ROUND(AVG(t.IsFraud) * 100, 2) AS Fraud_Rate_Pct,
    ROUND(SUM(t.FraudLossAmount), 2) AS Incurred_Loss_INR
FROM fact_transactions t
GROUP BY t.IPCountry, t.IsVPNorProxy
ORDER BY Incurred_Loss_INR DESC;

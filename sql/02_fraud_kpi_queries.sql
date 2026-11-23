-- ====================================================================
-- PROJECT: FinGuard - Digital Payment Fraud Analytics
-- SCRIPT: 02_fraud_kpi_queries.sql
-- DESCRIPTION: Core Executive Fraud KPIs, Loss Attribution, & Channel Mix
-- ====================================================================

-- KPI 1: Overall Platform Summary (Volume, Fraud Rate by Count & Amount, Chargeback Ratio)
SELECT 
    COUNT(t.TransactionID) AS Total_Transactions,
    ROUND(SUM(t.Amount), 2) AS Gross_Transaction_Value,
    SUM(t.IsFraud) AS Fraud_Transactions_Count,
    ROUND(AVG(t.IsFraud) * 100, 2) AS Fraud_Rate_Pct_Count,
    ROUND(SUM(t.FraudLossAmount), 2) AS Net_Fraud_Incurred_Loss,
    ROUND(SUM(t.PreventedLossAmount), 2) AS Fraud_Loss_Prevented,
    ROUND((SUM(t.FraudLossAmount) / NULLIF(SUM(t.Amount), 0)) * 100, 3) AS Fraud_Rate_Pct_Value,
    COUNT(CASE WHEN t.ChargebackStatus LIKE '%Chargeback%' THEN 1 END) AS Total_Chargebacks,
    ROUND((COUNT(CASE WHEN t.ChargebackStatus LIKE '%Chargeback%' THEN 1 END) * 1.0 / COUNT(t.TransactionID)) * 100, 2) AS Chargeback_Rate_Pct
FROM fact_transactions t;

-- KPI 2: Monthly Trends in Incurred Fraud Loss vs Rule Engine Prevention
SELECT 
    d.YearMonth,
    d.MonthName,
    COUNT(t.TransactionID) AS Monthly_Volume,
    ROUND(SUM(t.Amount), 2) AS Total_GMV,
    ROUND(SUM(t.FraudLossAmount), 2) AS Incurred_Loss,
    ROUND(SUM(t.PreventedLossAmount), 2) AS Prevented_Loss,
    ROUND(
        (SUM(t.PreventedLossAmount) / NULLIF(SUM(t.FraudLossAmount) + SUM(t.PreventedLossAmount), 0)) * 100, 2
    ) AS Prevention_Efficiency_Pct
FROM fact_transactions t
JOIN dim_date d ON t.TransactionDate = d.Date
GROUP BY d.YearMonth, d.MonthName
ORDER BY d.YearMonth;

-- KPI 3: Fraud Risk and Loss by Payment Channel
SELECT 
    t.PaymentMethod,
    COUNT(t.TransactionID) AS Total_Attempts,
    SUM(t.IsFraud) AS Fraud_Attempts,
    ROUND(AVG(t.IsFraud) * 100, 2) AS Fraud_Rate_Pct,
    ROUND(SUM(t.Amount), 2) AS Total_Payment_Value,
    ROUND(SUM(t.FraudLossAmount), 2) AS Incurred_Fraud_Loss,
    ROUND(AVG(t.RiskScore), 1) AS Avg_Risk_Score
FROM fact_transactions t
GROUP BY t.PaymentMethod
ORDER BY Incurred_Fraud_Loss DESC;

-- KPI 4: Attack Vector Distribution (Card Testing, Account Takeover, Friendly Fraud, etc.)
SELECT 
    t.FraudType,
    COUNT(*) AS Incident_Count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS Pct_Of_All_Fraud,
    ROUND(SUM(t.FraudLossAmount), 2) AS Total_Loss_INR,
    ROUND(AVG(t.Amount), 2) AS Avg_Ticket_Size_INR
FROM fact_transactions t
WHERE t.IsFraud = 1
GROUP BY t.FraudType
ORDER BY Incident_Count DESC;

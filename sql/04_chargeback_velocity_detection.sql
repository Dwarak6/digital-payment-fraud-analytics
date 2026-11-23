-- ====================================================================
-- PROJECT: FinGuard - Digital Payment Fraud Analytics
-- SCRIPT: 04_chargeback_velocity_detection.sql
-- DESCRIPTION: Window Functions for Velocity Attack Detection (Card Testing / Rapid-fire bursts)
-- ====================================================================

-- 1. Velocity Abuse Detection: Customers with > 3 Transactions Within a 10-Minute Window
WITH OrderedTransactions AS (
    SELECT 
        TransactionID,
        CustomerID,
        MerchantID,
        Amount,
        PaymentMethod,
        TransactionTimestamp,
        IsFraud,
        RiskScore,
        LAG(TransactionTimestamp, 1) OVER (PARTITION BY CustomerID ORDER BY TransactionTimestamp) AS Prev_Tx_1,
        LAG(TransactionTimestamp, 2) OVER (PARTITION BY CustomerID ORDER BY TransactionTimestamp) AS Prev_Tx_2,
        LAG(TransactionTimestamp, 3) OVER (PARTITION BY CustomerID ORDER BY TransactionTimestamp) AS Prev_Tx_3
    FROM fact_transactions
),
VelocityBursts AS (
    SELECT 
        TransactionID,
        CustomerID,
        TransactionTimestamp,
        Amount,
        IsFraud,
        RiskScore,
        ROUND(EXTRACT(EPOCH FROM (TransactionTimestamp - Prev_Tx_3)) / 60.0, 2) AS Minutes_Between_4_Txs
    FROM OrderedTransactions
    WHERE Prev_Tx_3 IS NOT NULL
)
SELECT 
    CustomerID,
    TransactionID,
    TransactionTimestamp,
    Amount,
    IsFraud,
    RiskScore,
    Minutes_Between_4_Txs,
    'FLAGGED: Rapid Velocity Spike' AS Investigation_Reason
FROM VelocityBursts
WHERE Minutes_Between_4_Txs <= 10.0
ORDER BY Minutes_Between_4_Txs ASC;

-- 2. Card Testing Pattern: Small Micro-Transactions followed by an Immediate High-Ticket Transaction
WITH TxLeadLag AS (
    SELECT 
        CustomerID,
        TransactionID,
        Amount,
        PaymentMethod,
        TransactionTimestamp,
        IsFraud,
        LAG(Amount, 1) OVER (PARTITION BY CustomerID, PaymentMethod ORDER BY TransactionTimestamp) AS Prev_Amount,
        LEAD(Amount, 1) OVER (PARTITION BY CustomerID, PaymentMethod ORDER BY TransactionTimestamp) AS Next_Amount,
        EXTRACT(EPOCH FROM (TransactionTimestamp - LAG(TransactionTimestamp, 1) OVER (PARTITION BY CustomerID, PaymentMethod ORDER BY TransactionTimestamp))) / 60.0 AS Mins_Since_Prev
    FROM fact_transactions
)
SELECT 
    CustomerID,
    TransactionID,
    PaymentMethod,
    Prev_Amount AS Preceding_Micro_Tx_Amount,
    Amount AS Suspect_Surge_Amount,
    ROUND(Mins_Since_Prev, 2) AS Elapsed_Minutes,
    IsFraud
FROM TxLeadLag
WHERE Prev_Amount < 150.00 
  AND Amount > 25000.00 
  AND Mins_Since_Prev <= 15.0
ORDER BY Elapsed_Minutes ASC;

-- ====================================================================
-- PROJECT: FinGuard - Digital Payment Fraud Analytics
-- SCRIPT: 01_schema_and_star_model.sql
-- DESCRIPTION: DDL definitions for Star Schema in Snowflake / PostgreSQL / BigQuery
-- ====================================================================

-- 1. Create Dimension: dim_customer
CREATE TABLE IF NOT EXISTS dim_customer (
    CustomerID VARCHAR(30) PRIMARY KEY,
    CustomerSegment VARCHAR(50),
    City VARCHAR(50),
    State VARCHAR(50),
    Region VARCHAR(30),
    Age INT,
    SignupDate DATE,
    KYCStatus VARCHAR(30),
    CreditScoreTier VARCHAR(30),
    AccountRiskWeight NUMERIC(5, 3)
);

-- 2. Create Dimension: dim_merchant
CREATE TABLE IF NOT EXISTS dim_merchant (
    MerchantID VARCHAR(30) PRIMARY KEY,
    MerchantName VARCHAR(100),
    MerchantCategory VARCHAR(50),
    RiskTier VARCHAR(30),
    BaseFraudRate NUMERIC(5, 3),
    SettlementPeriodDays INT,
    ChargebackThresholdPct NUMERIC(5, 2)
);

-- 3. Create Dimension: dim_date
CREATE TABLE IF NOT EXISTS dim_date (
    Date DATE PRIMARY KEY,
    Year INT,
    Quarter VARCHAR(5),
    YearQuarter VARCHAR(10),
    Month INT,
    MonthName VARCHAR(20),
    YearMonth VARCHAR(10),
    Day INT,
    DayOfWeek VARCHAR(20),
    DayOfWeekNumber INT,
    IsWeekend INT
);

-- 4. Create Fact Table: fact_transactions
CREATE TABLE IF NOT EXISTS fact_transactions (
    TransactionID VARCHAR(40) PRIMARY KEY,
    TransactionTimestamp TIMESTAMP,
    TransactionDate DATE REFERENCES dim_date(Date),
    TransactionHour INT,
    CustomerID VARCHAR(30) REFERENCES dim_customer(CustomerID),
    MerchantID VARCHAR(30) REFERENCES dim_merchant(MerchantID),
    PaymentMethod VARCHAR(50),
    DeviceType VARCHAR(50),
    IPCountry VARCHAR(50),
    IsVPNorProxy INT,
    Amount NUMERIC(12, 2),
    TransactionStatus VARCHAR(50),
    IsStatusCompleted INT,
    RiskScore NUMERIC(5, 1),
    RiskBand VARCHAR(30),
    IsFraud INT,
    FraudType VARCHAR(50),
    ChargebackStatus VARCHAR(50),
    FraudLossAmount NUMERIC(12, 2),
    PreventedLossAmount NUMERIC(12, 2)
);

-- Create Indexes for Analytical Performance
CREATE INDEX idx_tx_date ON fact_transactions(TransactionDate);
CREATE INDEX idx_tx_customer ON fact_transactions(CustomerID);
CREATE INDEX idx_tx_merchant ON fact_transactions(MerchantID);
CREATE INDEX idx_tx_fraud ON fact_transactions(IsFraud);
CREATE INDEX idx_tx_riskband ON fact_transactions(RiskBand);

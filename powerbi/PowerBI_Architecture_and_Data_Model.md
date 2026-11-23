# FinGuard Power BI Data Model & Architecture Specification

## 1. Relational Architecture (Star Schema)

The reporting layer uses a high-performance **Star Schema** with 1 centralized Fact table and 3 Dimension tables.

```
       +-------------------------+
       |   powerbi_dim_date      |
       +-------------------------+
       | * Date (PK)             |
       |   Year, Quarter, Month  |
       +------------+------------+
                    | (1:*)
                    v
+-------------------------+         +-------------------------------+
|  powerbi_dim_customers  |         |   powerbi_fact_transactions   |         +-----------------------+
+-------------------------+         +-------------------------------+         | powerbi_dim_merchants |
| * CustomerID (PK)       | (1:*)   | * TransactionID (PK)          |  (*:1)  +-----------------------+
|   CustomerSegment       +-------->|   TransactionDate (FK)        |<--------+ * MerchantID (PK)     |
|   KYCStatus, CreditTier |         |   CustomerID (FK)             |         |   MerchantName        |
+-------------------------+         |   MerchantID (FK)             |         |   MerchantCategory    |
                                    |   Amount, RiskScore           |         |   RiskTier, Threshold |
                                    |   IsFraud, ChargebackStatus   |         +-----------------------+
                                    +-------------------------------+
```

## 2. Table Specifications & Relationships

| Source File | Table Name in Power BI | Primary Key (PK) / Foreign Key (FK) | Target Table | Relationship Cardinality | Cross Filter Direction |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `powerbi_fact_transactions.csv` | `powerbi_fact_transactions` | `TransactionID` (PK) | - | - | - |
| `powerbi_dim_date.csv` | `powerbi_dim_date` | `Date` (PK) | `fact_transactions` (`TransactionDate`) | 1 to Many (1:*) | Single (Date filters Fact) |
| `powerbi_dim_customers.csv` | `powerbi_dim_customers` | `CustomerID` (PK) | `fact_transactions` (`CustomerID`) | 1 to Many (1:*) | Single (Customer filters Fact) |
| `powerbi_dim_merchants.csv` | `powerbi_dim_merchants` | `MerchantID` (PK) | `fact_transactions` (`MerchantID`) | 1 to Many (1:*) | Single (Merchant filters Fact) |

## 3. Date Table Configuration
- In Power BI Model View, right-click `powerbi_dim_date` and select **Mark as Date Table**.
- Select the column `Date`.
- Sort `MonthName` by `Month` column to guarantee chronological sorting (Jan, Feb, Mar...).
- Sort `DayOfWeek` by `DayOfWeekNumber`.

## 4. Column Data Types & Formats
- `Amount`, `FraudLossAmount`, `PreventedLossAmount`: Currency (`INR ₹` or `$`), 2 decimal places.
- `RiskScore`: Decimal Number, 1 decimal place.
- `TransactionTimestamp`: Date/Time.
- `IsFraud`, `IsVPNorProxy`, `IsStatusCompleted`: Whole Number (0 or 1).
- `Fraud Rate % (Count)`, `Chargeback Rate %`, `Rule Engine Prevention Efficiency %`: Percentage (`%`), 2 decimal places.

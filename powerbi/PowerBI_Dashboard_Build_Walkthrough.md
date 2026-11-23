# Power BI Dashboard Build Walkthrough: FinGuard Fraud Analytics

Follow this step-by-step tutorial to build the 3-page interactive Power BI dashboard in **Power BI Desktop**.

---

## Step 1: Ingesting the Processed Data
1. Launch **Power BI Desktop**.
2. Click **Get Data** -> **Text/CSV**.
3. Navigate to `data/processed/` and import the following 4 files:
   - `powerbi_fact_transactions.csv`
   - `powerbi_dim_customers.csv`
   - `powerbi_dim_merchants.csv`
   - `powerbi_dim_date.csv`
4. Click **Transform Data** (Power Query) to inspect column types:
   - Ensure `TransactionDate` and `Date` are set to `Date`.
   - Ensure `Amount`, `FraudLossAmount`, `PreventedLossAmount` are `Fixed Decimal Number` (Currency).
   - Ensure `RiskScore` is `Decimal Number`.
5. Click **Close & Apply**.

---

## Step 2: Establish Model Relationships
1. Switch to the **Model View** (left navigation bar icon).
2. Create active `1:*` relationships:
   - `powerbi_dim_date[Date]` -> `powerbi_fact_transactions[TransactionDate]`
   - `powerbi_dim_customers[CustomerID]` -> `powerbi_fact_transactions[CustomerID]`
   - `powerbi_dim_merchants[MerchantID]` -> `powerbi_fact_transactions[MerchantID]`
3. Right-click `powerbi_dim_date` -> **Mark as date table** -> Choose `Date`.
4. In `powerbi_dim_date`, select `MonthName` column -> Click **Column Tools** -> **Sort by Column** -> select `Month`.

---

## Step 3: Import Custom Theme
1. Navigate to the top ribbon: **View** tab -> **Themes** dropdown.
2. Click **Browse for themes**.
3. Select `powerbi/color_palette.json`.
4. This instantly configures the sleek dark background (`#0B0F19`), modern card styling (`#1E293B`), and fintech color palette.

---

## Step 4: Add DAX Measures
1. Click **Modeling** tab -> **New Table** -> Name it `_Measures`.
2. Open `powerbi/DAX_Measures.dax`.
3. Add the key measures into `_Measures`:
   - `[Total Transactions]`
   - `[Total GMV]`
   - `[Total Incurred Fraud Loss]`
   - `[Total Prevented Fraud Loss]`
   - `[Fraud Rate % (Count)]`
   - `[Chargeback Rate %]`
   - `[Rule Engine Prevention Efficiency %]`

---

## Step 5: Constructing Page 1 - Executive Fraud Overview
- **Header**: Add a Text Box: `FinGuard | Digital Payment Fraud & Risk Analytics Dashboard`.
- **Top Row KPI Cards** (New Card Visual):
  1. Card 1: `Total GMV` (Display units: Millions or Billions).
  2. Card 2: `Total Incurred Fraud Loss` (Callout value color: `#EF4444`).
  3. Card 3: `Total Prevented Fraud Loss` (Callout value color: `#10B981`).
  4. Card 4: `Chargeback Rate %` (Callout value color: `#F59E0B`).
- **Visual 1: Area / Line Chart (Center Left)**:
  - X-Axis: `powerbi_dim_date[MonthName]`
  - Y-Axis: `[Total GMV]` and `[Total Incurred Fraud Loss]`
  - Format: Line width = 3, data markers enabled.
- **Visual 2: Horizontal Bar Chart (Center Right)**:
  - Y-Axis: `powerbi_fact_transactions[PaymentMethod]`
  - X-Axis: `[Fraud Rate % (Count)]`
  - Data Labels: On.
- **Visual 3: Column Chart (Bottom Left)**:
  - X-Axis: `powerbi_dim_merchants[MerchantCategory]`
  - Y-Axis: `[Total Incurred Fraud Loss]`
- **Visual 4: Donut Chart (Bottom Right)**:
  - Legend: `powerbi_fact_transactions[FraudType]` (filter out "None")
  - Values: `Count of TransactionID`

---

## Step 6: Constructing Page 2 - Merchant Risk & Chargebacks
- **Visual 1: Scatter Chart**:
  - X-Axis: `[Total Transactions]`
  - Y-Axis: `[Chargeback Rate %]`
  - Size: `[Total Incurred Fraud Loss]`
  - Legend: `powerbi_dim_merchants[RiskTier]`
  - Constant Line: Add an X/Y constant line at `1.0%` with dashed red line (`#EF4444`) labeled `Visa/MC 1% Threshold`.
- **Visual 2: Risk Table / Matrix (Right side)**:
  - Rows: `MerchantName`, `MerchantCategory`, `RiskTier`
  - Values: `[Total GMV]`, `[Chargeback Rate %]`, `[Total Incurred Fraud Loss]`
  - Conditional Formatting: Background color on `Chargeback Rate %` where values `>= 1.0%` highlight in soft red.

---

## Step 7: Constructing Page 3 - Anomaly & Risk Investigation
- **Slicers (Top Ribbon)**:
  - `RiskBand` (Low, Medium, High)
  - `IsVPNorProxy` (0 or 1)
  - `DeviceType`
- **Visual 1: Hourly Attack Histogram**:
  - X-Axis: `TransactionHour` (0 to 23)
  - Y-Axis: `[Fraud Rate % (Count)]`
- **Visual 2: Transaction Investigation Drill-Down Table**:
  - Columns: `TransactionID`, `TransactionTimestamp`, `CustomerID`, `Amount`, `RiskScore`, `IsVPNorProxy`, `FraudType`, `TransactionStatus`.
  - Filter: Default to `RiskScore > 70`.

---

## Step 8: Taking Screenshots for LinkedIn & GitHub
1. In Power BI Desktop, click **View** -> **Page View** -> **Fit to Page** or **Actual Size**.
2. Maximize window or export to PDF (`File -> Export -> Export to PDF`).
3. Take high-resolution full-screen snips (`Win + Shift + S`) or use the generated images in `images/`!

# LinkedIn Document Carousel Blueprint (7 Slides)

Document carousels (PDF uploads) consistently receive 3x to 5x higher reach on LinkedIn because readers spend time swiping through them.

You can paste these slide contents into **Canva** (using standard 1080x1350px or 1080x1080px format), download as a PDF, and upload it as a Document on LinkedIn!

---

### Slide 1: Cover (Hook)
- **Top Badge**: 🛡️ FINTECH & FRAUD ANALYTICS
- **Big Title**: How to Build a Payment Fraud Intelligence Dashboard
- **Subtitle**: From 45,000 Raw Transactions to ₹2.2 Cr Loss Prevention
- **Visual**: Mini thumbnail preview of `dashboard_executive_overview.png`
- **Bottom Callout**: Swipe to see the architecture & insights ➔

---

### Slide 2: The Problem Statement
- **Headline**: The High Stakes of Digital Payment Fraud
- **Bullet 1**: Digital payments grow 25% YoY, but fraud tactics are evolving faster than legacy rules.
- **Bullet 2**: The Challenge: Blocking fraud without causing false positives that anger legitimate customers.
- **Bullet 3**: The Compliance Threat: Exceeding a 1.0% chargeback ratio triggers severe scheme penalties and fines.

---

### Slide 3: The Data Architecture (Star Schema)
- **Headline**: Foundation: Designing the Star Schema
- **Visual**: Diagram showing `fact_transactions` surrounded by `dim_customer`, `dim_merchant`, `dim_date`.
- **Key Takeaway**: A normalized Star Schema reduces DAX overhead, speeds up cross-filtering, and simplifies drill-throughs in Power BI.

---

### Slide 4: SQL Deep Dive: Velocity & Card Testing Detection
- **Headline**: Detecting Stealth Attacks with SQL Window Functions
- **Code Snippet**:
  ```sql
  -- Detecting 4 transactions within 10 minutes
  LAG(TransactionTimestamp, 3) 
    OVER (PARTITION BY CustomerID ORDER BY TransactionTimestamp)
  ```
- **Finding**: Identified rapid-fire micro-transactions ($1 tests followed by $500 fraud spikes).

---

### Slide 5: Machine Learning & Risk Optimization
- **Headline**: Beyond Static Rules: Machine Learning Risk Scoring
- **Model**: Balanced Random Forest Classifier (0.73 ROC-AUC).
- **Top 3 Predictive Features**:
  1. VPN / Anonymizer Proxy (19.7% weight)
  2. Transaction Amount Anomaly (17.1% weight)
  3. Off-Peak Night Window: 00:00 - 05:00 (8.6% weight)
- **Cost Matrix**: Net saving of ₹2.23 Cr while budgeting for user friction costs.

---

### Slide 6: The Power BI Dashboard in Action
- **Headline**: Executive Risk & Governance Dashboard
- **Visual**: Full-bleed high-res screenshot of `dashboard_executive_overview.png`.
- **Key Features Highlighted**:
  - Live KPI Callouts (GMV, Fraud Loss, Chargeback Ratio)
  - Monthly Volume vs Loss Trends
  - High-Risk Merchant Scatter Matrix (1.0% limit line)

---

### Slide 7: Conclusion & Key Learnings
- **Headline**: What This Project Taught Me
- **Takeaway 1**: Great analytics bridges data engineering, statistical modeling, and business risk.
- **Takeaway 2**: Power BI DAX + Star Schema delivers instant executive visibility.
- **CTA**: Full code, SQL queries & Power BI dataset available on GitHub!
- **Callout**: Link in the post caption / comments!

"""
Generate High-Quality PDF Reports and LinkedIn Carousel PDF
Uses matplotlib.backends.backend_pdf.PdfPages to compile executive report and LinkedIn carousel.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg
import pandas as pd
import numpy as np

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(PROJECT_DIR, "docs")
IMG_DIR = os.path.join(PROJECT_DIR, "images")
os.makedirs(DOCS_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

def create_executive_report_pdf():
    pdf_path = os.path.join(DOCS_DIR, "FinGuard_Executive_Fraud_Analytics_Report.pdf")
    print(f"Creating Executive Report PDF at: {pdf_path}")
    
    with PdfPages(pdf_path) as pdf:
        # ---------------- PAGE 1: COVER PAGE ----------------
        fig = plt.figure(figsize=(11.69, 8.27), facecolor='#0B0F19') # A4 Landscape
        ax = fig.add_axes([0, 0, 1, 1], facecolor='#0B0F19')
        ax.axis('off')
        
        # Design accents
        ax.fill_between([0, 1], [0.82, 0.82], [1.0, 1.0], color='#1E293B', transform=ax.transAxes)
        ax.plot([0, 1], [0.82, 0.82], color='#3B82F6', linewidth=3, transform=ax.transAxes)
        
        ax.text(0.08, 0.90, "FINTECH INTELLIGENCE & RISK GOVERNANCE REPORT", color='#38BDF8', fontsize=13, fontweight='bold', transform=ax.transAxes)
        ax.text(0.08, 0.68, "FinGuard: Digital Payment Fraud\n& Transaction Risk Analytics", color='#FFFFFF', fontsize=26, fontweight='bold', transform=ax.transAxes)
        ax.text(0.08, 0.54, "An End-to-End Analytics Portfolio Project on 45,000+ Transactions", color='#94A3B8', fontsize=15, transform=ax.transAxes)
        
        # Highlights box
        box_text = (
            "EXECUTIVE REPORT HIGHLIGHTS:\n\n"
            "• Analyzed 45,000 transactions across 10 merchant categories\n"
            "• ₹8.60 Cr in incurred fraud losses & ₹3.74 Cr in intercepted attempts\n"
            "• Machine Learning Risk Scoring: ₹2.23 Cr net prevention savings\n"
            "• Regulatory Compliance: Identified 8.5% of merchants breaching 1.0% chargeback limit\n"
            "• Multi-Channel Intelligence: High-risk nocturnal window (00:00 - 05:00 AM)"
        )
        ax.text(0.08, 0.22, box_text, color='#E2E8F0', fontsize=11, transform=ax.transAxes,
                bbox=dict(boxstyle='round,pad=1.2', facecolor='#1E293B', edgecolor='#334155', linewidth=1.5))
        
        ax.text(0.08, 0.08, "Author: Data Analyst Portfolio  |  Tools: SQL, Python, Scikit-Learn, Power BI, DAX  |  Year: FY 2025", color='#64748B', fontsize=10, transform=ax.transAxes)
        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()
        
        # ---------------- PAGE 2: POWER BI EXECUTIVE DASHBOARD ----------------
        fig = plt.figure(figsize=(11.69, 8.27), facecolor='#0B0F19')
        ax = fig.add_axes([0, 0, 1, 1], facecolor='#0B0F19')
        ax.axis('off')
        
        img1 = mpimg.imread(os.path.join(IMG_DIR, "dashboard_executive_overview.png"))
        ax.imshow(img1, extent=[0.03, 0.97, 0.08, 0.90])
        ax.text(0.05, 0.93, "SECTION 1: POWER BI EXECUTIVE DASHBOARD (PAGE 1)", color='#38BDF8', fontsize=13, fontweight='bold', transform=ax.transAxes)
        ax.text(0.05, 0.04, "Figure 1.1: Core platform metrics, monthly volume vs fraud loss trends, and attack distribution.", color='#94A3B8', fontsize=9.5, transform=ax.transAxes)
        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()

        # ---------------- PAGE 3: MERCHANT RISK & CHARGEBACKS ----------------
        fig = plt.figure(figsize=(11.69, 8.27), facecolor='#0B0F19')
        ax = fig.add_axes([0, 0, 1, 1], facecolor='#0B0F19')
        ax.axis('off')
        
        img2 = mpimg.imread(os.path.join(IMG_DIR, "dashboard_merchant_deepdive.png"))
        ax.imshow(img2, extent=[0.03, 0.97, 0.08, 0.90])
        ax.text(0.05, 0.93, "SECTION 2: MERCHANT RISK & CHARGEBACK MONITORING (PAGE 2)", color='#38BDF8', fontsize=13, fontweight='bold', transform=ax.transAxes)
        ax.text(0.05, 0.04, "Figure 2.1: Transaction volume vs dispute ratio against the 1.0% card scheme penalty threshold.", color='#94A3B8', fontsize=9.5, transform=ax.transAxes)
        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()

        # ---------------- PAGE 4: SQL & ML RISK MODELING ----------------
        fig = plt.figure(figsize=(11.69, 8.27), facecolor='#0B0F19')
        ax = fig.add_axes([0, 0, 1, 1], facecolor='#0B0F19')
        ax.axis('off')
        
        img3 = mpimg.imread(os.path.join(IMG_DIR, "fraud_trend_analysis.png"))
        ax.imshow(img3, extent=[0.05, 0.95, 0.40, 0.88])
        ax.text(0.05, 0.93, "SECTION 3: TRANSACTION VELOCITY & PREDICTIVE MODELING", color='#38BDF8', fontsize=13, fontweight='bold', transform=ax.transAxes)
        
        # Summary Table of Machine Learning Cost Matrix
        ml_summary = (
            "MACHINE LEARNING RISK SCORING & COST MATRIX EVALUATION:\n\n"
            "• Model Architecture: Balanced Random Forest Classifier (0.7291 ROC-AUC)\n"
            "• Primary Risk Features: VPN/Proxy Concealment (19.7%), Transaction Amount (17.1%), Nocturnal Window (8.6%)\n"
            "• Gross Fraud Loss Prevented: ₹22,556,369.24 (~₹2.25 Cr)\n"
            "• Customer Friction Cost (False Positives @ ₹150): ₹248,550.00\n"
            "• Net Financial Impact (Savings minus Friction): ₹22,307,819.24 (~₹2.23 Cr)\n\n"
            "SQL VELOCITY DETECTION HIGHLIGHT:\n"
            "Window functions (LAG) flagged card-testing bursts: micro-transactions (< ₹150) followed immediately by large charges (> ₹25,000)."
        )
        ax.text(0.05, 0.06, ml_summary, color='#E2E8F0', fontsize=10.5, transform=ax.transAxes,
                bbox=dict(boxstyle='round,pad=1.0', facecolor='#1E293B', edgecolor='#334155', linewidth=1.5))
        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()

        # ---------------- PAGE 5: STRATEGIC ROADMAP ----------------
        fig = plt.figure(figsize=(11.69, 8.27), facecolor='#0B0F19')
        ax = fig.add_axes([0, 0, 1, 1], facecolor='#0B0F19')
        ax.axis('off')
        
        ax.text(0.08, 0.90, "SECTION 4: STRATEGIC RISK GOVERNANCE & ACTION PLAN", color='#38BDF8', fontsize=14, fontweight='bold', transform=ax.transAxes)
        
        recs = [
            ("1. Dynamic Authentication (3DS Frictionless vs Challenge)",
             "Apply frictionless flow for low-risk transactions (Risk Score < 30). Trigger step-up biometric/OTP challenge only for transactions in the nocturnal window (00:00 - 05:00) or originating from masked VPN/proxy IP addresses."),
            ("2. Merchant Escrow Hold & Tiered Payouts",
             "For merchants approaching a 0.75% dispute threshold, institute a rolling 5% escrow reserve. Merchants breaching the 1.0% scheme limit must be placed on immediate 14-day settlement delay to cushion acquirer exposure."),
            ("3. Real-Time Card Testing Velocity Blockers",
             "Deploy Redis / Kafka in-memory sliding counters to automatically pause card checkout attempts if more than 3 transactions occur within 10 minutes on the same card hash or device fingerprint."),
            ("4. KYC & High-Risk Category Hardening",
             "Enforce biometric video KYC for accounts purchasing in Crypto and Luxury segments, which historically represent the highest ticket loss concentration (averaging > ₹35,000 per incident).")
        ]
        
        y_pos = 0.76
        for title, desc in recs:
            ax.text(0.08, y_pos, title, color='#10B981', fontsize=12, fontweight='bold', transform=ax.transAxes)
            ax.text(0.08, y_pos - 0.07, desc, color='#CBD5E1', fontsize=10, transform=ax.transAxes, wrap=True)
            y_pos -= 0.17
            
        ax.text(0.08, 0.06, "End of Report  |  FinGuard Digital Payment Analytics  |  Complete code and data available on GitHub", color='#64748B', fontsize=10, transform=ax.transAxes)
        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()

    print("Executive Report PDF successfully generated.")

def create_linkedin_carousel_pdf():
    pdf_path = os.path.join(DOCS_DIR, "FinGuard_LinkedIn_Carousel_Document.pdf")
    print(f"Creating LinkedIn Carousel PDF at: {pdf_path}")
    
    # 1080 x 1350 aspect ratio (4:5 vertical portrait, best for LinkedIn Document Posts)
    w_in = 8.5
    h_in = 10.625
    
    with PdfPages(pdf_path) as pdf:
        # SLIDE 1: COVER
        fig = plt.figure(figsize=(w_in, h_in), facecolor='#0B0F19')
        ax = fig.add_axes([0, 0, 1, 1], facecolor='#0B0F19')
        ax.axis('off')
        
        ax.text(0.08, 0.88, "🛡️ FINTECH & FRAUD ANALYTICS", color='#38BDF8', fontsize=14, fontweight='bold', transform=ax.transAxes)
        ax.text(0.08, 0.75, "How to Build a\nPayment Fraud\nIntelligence\nDashboard", color='#FFFFFF', fontsize=32, fontweight='bold', transform=ax.transAxes)
        ax.text(0.08, 0.58, "From 45,000 Raw Transactions\nto ₹2.23 Cr Net Fraud Prevention", color='#94A3B8', fontsize=16, transform=ax.transAxes)
        
        img = mpimg.imread(os.path.join(IMG_DIR, "dashboard_executive_overview.png"))
        ax.imshow(img, extent=[0.08, 0.92, 0.18, 0.52])
        
        ax.text(0.08, 0.10, "SWIPE TO SEE THE ARCHITECTURE & CODE ➔", color='#10B981', fontsize=13, fontweight='bold', transform=ax.transAxes)
        ax.text(0.08, 0.05, "By Data Analyst  •  SQL | Python | Power BI | DAX", color='#64748B', fontsize=11, transform=ax.transAxes)
        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()
        
        # SLIDE 2: THE PROBLEM
        fig = plt.figure(figsize=(w_in, h_in), facecolor='#0B0F19')
        ax = fig.add_axes([0, 0, 1, 1], facecolor='#0B0F19')
        ax.axis('off')
        ax.text(0.08, 0.90, "01 / THE CHALLENGE", color='#38BDF8', fontsize=13, fontweight='bold', transform=ax.transAxes)
        ax.text(0.08, 0.80, "The High Stakes of\nPayment Fraud", color='#FFFFFF', fontsize=26, fontweight='bold', transform=ax.transAxes)
        
        points = [
            ("Global Exposure", "Digital payment fraud exceeds $38 Billion annually. Every ₹1 lost costs ₹3.50+ in administrative disputes and scheme fines."),
            ("The Friction Dilemma", "Overly aggressive fraud filters block honest customers, leading to cart abandonment and revenue churn."),
            ("The 1.0% Regulatory Threat", "Payment schemes (Visa/Mastercard) penalize merchants exceeding a 1.0% chargeback ratio with heavy fines and account closure.")
        ]
        y = 0.65
        for t, d in points:
            ax.text(0.08, y, f"• {t}", color='#F59E0B', fontsize=16, fontweight='bold', transform=ax.transAxes)
            ax.text(0.08, y - 0.06, d, color='#CBD5E1', fontsize=12, transform=ax.transAxes, wrap=True)
            y -= 0.16
        ax.text(0.08, 0.08, "Swipe for Data Architecture ➔", color='#94A3B8', fontsize=12, transform=ax.transAxes)
        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()

        # SLIDE 3: DATA ARCHITECTURE
        fig = plt.figure(figsize=(w_in, h_in), facecolor='#0B0F19')
        ax = fig.add_axes([0, 0, 1, 1], facecolor='#0B0F19')
        ax.axis('off')
        ax.text(0.08, 0.90, "02 / DATA ARCHITECTURE", color='#38BDF8', fontsize=13, fontweight='bold', transform=ax.transAxes)
        ax.text(0.08, 0.80, "Star Schema Design\nfor Power BI", color='#FFFFFF', fontsize=26, fontweight='bold', transform=ax.transAxes)
        
        schema_box = (
            "STAR SCHEMA ARCHITECTURE:\n\n"
            "1 Fact Table: `fact_transactions` (45,000 rows)\n"
            "  - Amount, RiskScore, IsFraud, ChargebackStatus, Loss\n\n"
            "3 Dimension Tables (1:* Relationships):\n"
            "  • `dim_customer`: Demographics, KYC, Credit Tier\n"
            "  • `dim_merchant`: Category, Risk Tier, 1% Limit\n"
            "  • `dim_date`: Time intelligence calendar\n\n"
            "Why Star Schema?\n"
            "✓ Optimizes Power BI VertiPaq compression\n"
            "✓ Slashes DAX query latency\n"
            "✓ Eliminates many-to-many ambiguity"
        )
        ax.text(0.08, 0.24, schema_box, color='#E2E8F0', fontsize=12.5, transform=ax.transAxes,
                bbox=dict(boxstyle='round,pad=1.2', facecolor='#1E293B', edgecolor='#3B82F6', linewidth=1.5))
        ax.text(0.08, 0.08, "Swipe for SQL Analysis ➔", color='#94A3B8', fontsize=12, transform=ax.transAxes)
        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()

        # SLIDE 4: SQL ANALYTICS
        fig = plt.figure(figsize=(w_in, h_in), facecolor='#0B0F19')
        ax = fig.add_axes([0, 0, 1, 1], facecolor='#0B0F19')
        ax.axis('off')
        ax.text(0.08, 0.90, "03 / SQL ANALYTICS", color='#38BDF8', fontsize=13, fontweight='bold', transform=ax.transAxes)
        ax.text(0.08, 0.80, "Catching Attacks with\nSQL Window Functions", color='#FFFFFF', fontsize=26, fontweight='bold', transform=ax.transAxes)
        
        sql_box = (
            "-- Detecting Card Testing Micro-Transactions\n"
            "LAG(Amount, 1) OVER (\n"
            "  PARTITION BY CustomerID, PaymentMethod \n"
            "  ORDER BY TransactionTimestamp\n"
            ") AS Prev_Amount\n\n"
            "Pattern Uncovered:\n"
            "Fraudsters run micro-charges (< ₹150) to test card\n"
            "validity, followed immediately by surges (> ₹25,000)\n"
            "within 10-15 minutes."
        )
        ax.text(0.08, 0.35, sql_box, color='#38BDF8', fontsize=12, transform=ax.transAxes,
                bbox=dict(boxstyle='round,pad=1.2', facecolor='#1E293B', edgecolor='#334155', linewidth=1.5))
        ax.text(0.08, 0.08, "Swipe for Machine Learning Results ➔", color='#94A3B8', fontsize=12, transform=ax.transAxes)
        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()

        # SLIDE 5: ML & ROI
        fig = plt.figure(figsize=(w_in, h_in), facecolor='#0B0F19')
        ax = fig.add_axes([0, 0, 1, 1], facecolor='#0B0F19')
        ax.axis('off')
        ax.text(0.08, 0.90, "04 / PREDICTIVE MODELING", color='#38BDF8', fontsize=13, fontweight='bold', transform=ax.transAxes)
        ax.text(0.08, 0.80, "Risk Scoring &\n₹2.23 Cr Net Benefit", color='#FFFFFF', fontsize=26, fontweight='bold', transform=ax.transAxes)
        
        ml_box = (
            "BALANCED RANDOM FOREST (0.73 ROC-AUC):\n\n"
            "Top Risk Drivers:\n"
            "1. VPN / Masked IP Proxy (19.7% weight)\n"
            "2. Transaction Amount Anomaly (17.1% weight)\n"
            "3. Nocturnal Hours: 00:00 - 05:00 (8.6% weight)\n\n"
            "Financial Cost-Matrix:\n"
            "• Gross Fraud Loss Prevented: ₹2.25 Cr\n"
            "• False Positive Friction Cost (@ ₹150): ₹2.48 Lakh\n"
            "• NET FINANCIAL BENEFIT: ₹2.23 Cr"
        )
        ax.text(0.08, 0.28, ml_box, color='#E2E8F0', fontsize=12.5, transform=ax.transAxes,
                bbox=dict(boxstyle='round,pad=1.2', facecolor='#1E293B', edgecolor='#10B981', linewidth=1.5))
        ax.text(0.08, 0.08, "Swipe for Power BI Dashboard ➔", color='#94A3B8', fontsize=12, transform=ax.transAxes)
        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()

        # SLIDE 6: POWER BI VISUALS
        fig = plt.figure(figsize=(w_in, h_in), facecolor='#0B0F19')
        ax = fig.add_axes([0, 0, 1, 1], facecolor='#0B0F19')
        ax.axis('off')
        ax.text(0.08, 0.92, "05 / EXECUTIVE BI", color='#38BDF8', fontsize=13, fontweight='bold', transform=ax.transAxes)
        ax.text(0.08, 0.84, "Interactive Power BI\nExecutive Suite", color='#FFFFFF', fontsize=24, fontweight='bold', transform=ax.transAxes)
        
        img = mpimg.imread(os.path.join(IMG_DIR, "dashboard_merchant_deepdive.png"))
        ax.imshow(img, extent=[0.05, 0.95, 0.26, 0.78])
        
        ax.text(0.08, 0.16, "Features 30+ dynamic DAX measures:\nMoving Averages, Incurred Loss, & 1.0% Chargeback Matrix.", color='#CBD5E1', fontsize=12, transform=ax.transAxes)
        ax.text(0.08, 0.08, "Swipe for Takeaways & Link ➔", color='#94A3B8', fontsize=12, transform=ax.transAxes)
        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()

        # SLIDE 7: CONCLUSION & CTA
        fig = plt.figure(figsize=(w_in, h_in), facecolor='#0B0F19')
        ax = fig.add_axes([0, 0, 1, 1], facecolor='#0B0F19')
        ax.axis('off')
        ax.text(0.08, 0.88, "06 / CONCLUSION", color='#38BDF8', fontsize=13, fontweight='bold', transform=ax.transAxes)
        ax.text(0.08, 0.75, "Summary &\nKey Takeaways", color='#FFFFFF', fontsize=30, fontweight='bold', transform=ax.transAxes)
        
        concl_box = (
            "WHAT THIS PROJECT DELIVERED:\n\n"
            "✓ Production-ready Star Schema data warehouse\n"
            "✓ Complex SQL window queries for fraud detection\n"
            "✓ Machine learning risk scoring & cost-benefit ROI\n"
            "✓ Executive Power BI dashboard with 30+ DAX formulas\n\n"
            "🔗 FULL REPOSITORY & CODE ON GITHUB:\n"
            "Check out the link in the post description or comments!\n\n"
            "Let's connect and discuss Data Analytics & Risk!"
        )
        ax.text(0.08, 0.22, concl_box, color='#E2E8F0', fontsize=13, transform=ax.transAxes,
                bbox=dict(boxstyle='round,pad=1.2', facecolor='#1E293B', edgecolor='#38BDF8', linewidth=1.5))
        ax.text(0.08, 0.08, "★ Save & Share this post if you found it useful!", color='#10B981', fontsize=13, fontweight='bold', transform=ax.transAxes)
        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()

    print("LinkedIn Carousel PDF successfully generated.")

if __name__ == "__main__":
    create_executive_report_pdf()
    create_linkedin_carousel_pdf()
    print("All PDF assets compiled into docs/ directory!")

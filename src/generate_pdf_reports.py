"""
High-Resolution PDF Report & LinkedIn Carousel Generator
Renders individual pixel-perfect slides and compiles them using Pillow into flawless multi-page PDFs.
Eliminates glyph errors, image distortions, and aspect ratio clipping.
"""

import os
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import pandas as pd
import numpy as np

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(PROJECT_DIR, "docs")
IMG_DIR = os.path.join(PROJECT_DIR, "images")
TEMP_SLIDES_DIR = os.path.join(DOCS_DIR, "temp_slides")
os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(TEMP_SLIDES_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#334155'

# ==============================================================================
# 1. EXECUTIVE REPORT (16:9 LANDSCAPE - 1920 x 1080)
# ==============================================================================

def build_exec_page1():
    # Cover & Executive Summary
    fig = plt.figure(figsize=(16, 9), facecolor='#0B0F19')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#0B0F19')
    ax.axis('off')

    # Top Accent Banner
    rect = patches.Rectangle((0, 0.88), 1, 0.12, facecolor='#1E293B', transform=ax.transAxes)
    ax.add_patch(rect)
    ax.plot([0, 1], [0.88, 0.88], color='#38BDF8', linewidth=3, transform=ax.transAxes)

    ax.text(0.06, 0.94, "FINTECH INTELLIGENCE & RISK GOVERNANCE REPORT", color='#38BDF8', fontsize=14, fontweight='bold', transform=ax.transAxes, va='center')
    ax.text(0.82, 0.94, "FY 2025 • PORTFOLIO CASE STUDY", color='#94A3B8', fontsize=11, fontweight='bold', transform=ax.transAxes, va='center')

    ax.text(0.06, 0.77, "FinGuard: Digital Payment Fraud\n& Transaction Risk Analytics", color='#FFFFFF', fontsize=28, fontweight='bold', transform=ax.transAxes, va='top')
    ax.text(0.06, 0.62, "An End-to-End Analytics & Business Intelligence Project on 45,000+ Transactions", color='#94A3B8', fontsize=14, transform=ax.transAxes)

    # 4 Highlight Metric Cards
    cards = [
        ("TOTAL GMV ANALYZED", "INR 53.4 Cr", "45,000 Transactions", "#3B82F6"),
        ("INCURRED FRAUD LOSS", "INR 8.60 Cr", "5,557 Incidents (12.3%)", "#EF4444"),
        ("NET ML SAVINGS", "INR 2.23 Cr", "After Friction Deduction", "#10B981"),
        ("DISPUTE RISK MERCHANTS", "8.5%", "Breached 1.0% Threshold", "#F59E0B")
    ]
    for i, (title, val, sub, col) in enumerate(cards):
        cx = 0.06 + i * 0.225
        card_rect = patches.FancyBboxPatch((cx, 0.44), 0.205, 0.14, boxstyle="round,pad=0.01", facecolor='#1E293B', edgecolor=col, linewidth=1.5, transform=ax.transAxes)
        ax.add_patch(card_rect)
        ax.text(cx + 0.02, 0.54, title, color='#94A3B8', fontsize=9.5, fontweight='bold', transform=ax.transAxes)
        ax.text(cx + 0.02, 0.485, val, color='#FFFFFF', fontsize=17, fontweight='bold', transform=ax.transAxes)
        ax.text(cx + 0.02, 0.455, sub, color=col, fontsize=9.5, transform=ax.transAxes)

    # Executive Summary Paragraphs
    summary_text = (
        "EXECUTIVE SUMMARY & BUSINESS PROBLEM STATEMENT:\n\n"
        "Digital payment processors face an asymmetric financial challenge: every rupee lost to fraudulent checkout activity\n"
        "incurs over 3.5x in secondary expenses, including card scheme compliance penalties, chargeback administration, and churn.\n\n"
        "This project models an enterprise Star Schema data pipeline to analyze transaction velocity, payment channel vulnerabilities,\n"
        "and merchant risk. By coupling SQL window functions with Random Forest risk scoring, we isolated an off-peak nocturnal attack\n"
        "window (2.4x fraud spike), flagged card testing patterns, and evaluated a cost matrix delivering INR 2.23 Cr net prevention savings."
    )
    ax.text(0.06, 0.38, summary_text, color='#E2E8F0', fontsize=11.5, transform=ax.transAxes, va='top',
            bbox=dict(boxstyle='round,pad=1.0', facecolor='#162032', edgecolor='#334155', linewidth=1.2))

    ax.text(0.06, 0.06, "Author: Dwarak6 (GitHub: dwarak6)  |  Tools: SQL (PostgreSQL), Python (Pandas/Scikit-Learn), Power BI, DAX", color='#64748B', fontsize=10.5, transform=ax.transAxes)
    
    path = os.path.join(TEMP_SLIDES_DIR, "exec_p1.png")
    plt.savefig(path, dpi=150, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    return path

def build_exec_page_with_image(title_num, title_text, img_name, caption_text):
    # Load base screenshot
    img_path = os.path.join(IMG_DIR, img_name)
    base_img = Image.open(img_path).convert('RGB')
    
    # Create 1920x1080 canvas
    canvas = Image.new('RGB', (1920, 1080), color='#0B0F19')
    draw = ImageDraw.Draw(canvas)
    
    # Top Banner (1920 x 90)
    draw.rectangle([(0, 0), (1920, 90)], fill='#1E293B')
    draw.line([(0, 90), (1920, 90)], fill='#38BDF8', width=3)
    
    # Header Text
    header_str = f"SECTION {title_num}: {title_text.upper()}"
    draw.text((60, 25), header_str, fill='#38BDF8')
    draw.text((1500, 25), "FINGUARD RISK INTELLIGENCE", fill='#94A3B8')
    
    # Scale and paste image preserving 16:9 aspect ratio
    # Available area: width 1800, height 880 (from y=120 to y=1000)
    target_w = 1760
    target_h = int(target_w * (9 / 16)) # 990
    if target_h > 860:
        target_h = 860
        target_w = int(target_h * (16 / 9)) # 1528
        
    scaled_img = base_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    paste_x = (1920 - target_w) // 2
    paste_y = 120 + (860 - target_h) // 2
    
    # Border around image
    draw.rectangle([(paste_x - 3, paste_y - 3), (paste_x + target_w + 3, paste_y + target_h + 3)], outline='#38BDF8', width=2)
    canvas.paste(scaled_img, (paste_x, paste_y))
    
    # Caption Footer
    draw.rectangle([(0, 1030), (1920, 1080)], fill='#0F172A')
    draw.text((60, 1045), caption_text, fill='#CBD5E1')
    
    out_name = f"exec_{img_name}"
    out_path = os.path.join(TEMP_SLIDES_DIR, out_name)
    canvas.save(out_path, quality=95)
    return out_path

def build_exec_page5():
    # Strategic Roadmap
    fig = plt.figure(figsize=(16, 9), facecolor='#0B0F19')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#0B0F19')
    ax.axis('off')

    rect = patches.Rectangle((0, 0.88), 1, 0.12, facecolor='#1E293B', transform=ax.transAxes)
    ax.add_patch(rect)
    ax.plot([0, 1], [0.88, 0.88], color='#38BDF8', linewidth=3, transform=ax.transAxes)

    ax.text(0.06, 0.94, "SECTION 04: STRATEGIC RISK GOVERNANCE & ACTION PLAN", color='#38BDF8', fontsize=14, fontweight='bold', transform=ax.transAxes, va='center')
    ax.text(0.80, 0.94, "EXECUTIVE IMPLEMENTATION ROADMAP", color='#94A3B8', fontsize=11, fontweight='bold', transform=ax.transAxes, va='center')

    recs = [
        ("1. Dynamic Authentication (3DS Frictionless vs Challenge)",
         "Apply frictionless flow for low-risk transactions (Risk Score < 30). Trigger step-up biometric/OTP challenge only for transactions in the nocturnal window (00:00 - 05:00) or originating from masked VPN/proxy IP addresses."),
        ("2. Merchant Escrow Hold & Tiered Payouts",
         "For merchants approaching a 0.75% dispute threshold, institute a rolling 5% escrow reserve. Merchants breaching the 1.0% scheme limit must be placed on immediate 14-day settlement delay to cushion acquirer exposure."),
        ("3. Real-Time Card Testing Velocity Blockers",
         "Deploy Redis / Kafka in-memory sliding counters to automatically pause card checkout attempts if more than 3 transactions occur within 10 minutes on the same card hash or device fingerprint."),
        ("4. KYC & High-Risk Category Hardening",
         "Enforce biometric video KYC for accounts purchasing in Crypto and Luxury segments, which historically represent the highest ticket loss concentration (averaging > INR 35,000 per incident).")
    ]

    y_pos = 0.74
    for title, desc in recs:
        box = patches.FancyBboxPatch((0.06, y_pos - 0.12), 0.88, 0.13, boxstyle="round,pad=0.015", facecolor='#1E293B', edgecolor='#334155', linewidth=1.5, transform=ax.transAxes)
        ax.add_patch(box)
        ax.text(0.08, y_pos - 0.03, title, color='#10B981', fontsize=13, fontweight='bold', transform=ax.transAxes)
        ax.text(0.08, y_pos - 0.08, desc, color='#CBD5E1', fontsize=10.5, transform=ax.transAxes)
        y_pos -= 0.17

    ax.text(0.06, 0.05, "End of Executive Report  |  FinGuard Platform  |  Full Repository: https://github.com/Dwarak6/digital-payment-fraud-analytics", color='#64748B', fontsize=10.5, transform=ax.transAxes)

    path = os.path.join(TEMP_SLIDES_DIR, "exec_p5.png")
    plt.savefig(path, dpi=150, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    return path

def generate_executive_report_pdf():
    print("Building Executive Report pages...")
    p1 = build_exec_page1()
    p2 = build_exec_page_with_image(
        "01", "Power BI Executive Fraud & Loss Overview (Dashboard Page 1)",
        "dashboard_executive_overview.png",
        "Figure 1.1: Core platform KPIs, monthly volume vs fraud loss trends, payment method attack rate, and category losses."
    )
    p3 = build_exec_page_with_image(
        "02", "Merchant Risk & Chargeback Compliance Monitoring (Dashboard Page 2)",
        "dashboard_merchant_deepdive.png",
        "Figure 2.1: Transaction volume vs dispute ratio scatter matrix highlighting merchants breaching the 1.0% card scheme penalty ceiling."
    )
    p4 = build_exec_page_with_image(
        "03", "Transaction Velocity & Nocturnal Anomaly Analytics",
        "fraud_trend_analysis.png",
        "Figure 3.1: Hourly fraud concentration showing 2.4x nocturnal risk spike (00:00 - 05:00) and device/proxy vulnerability matrix."
    )
    p5 = build_exec_page5()

    pages = [Image.open(p).convert('RGB') for p in [p1, p2, p3, p4, p5]]
    
    pdf_out = os.path.join(DOCS_DIR, "FinGuard_Executive_Fraud_Analytics_Report.pdf")
    pages[0].save(pdf_out, save_all=True, append_images=pages[1:], resolution=150.0)
    print(f"Flawless Executive Report PDF compiled: {pdf_out}")

# ==============================================================================
# 2. LINKEDIN CAROUSEL (4:5 PORTRAIT - 1080 x 1350)
# ==============================================================================

def make_carousel_slide(slide_num, title, subtitle, bullets_or_box, is_cover=False, img_embed=None):
    fig = plt.figure(figsize=(8.64, 10.8), facecolor='#0B0F19') # 1080 x 1350 at 125 dpi
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#0B0F19')
    ax.axis('off')

    # Top Brand Header
    ax.text(0.08, 0.93, f"[FINTECH & FRAUD ANALYTICS]  •  SLIDE {slide_num}/7", color='#38BDF8', fontsize=11, fontweight='bold', transform=ax.transAxes)
    ax.plot([0.08, 0.92], [0.91, 0.91], color='#334155', linewidth=1.5, transform=ax.transAxes)

    if is_cover:
        ax.text(0.08, 0.82, "How to Build a\nPayment Fraud\nIntelligence\nDashboard", color='#FFFFFF', fontsize=26, fontweight='bold', transform=ax.transAxes, va='top')
        ax.text(0.08, 0.58, "From 45,000 Raw Transactions to\nINR 2.23 Cr Net Fraud Prevention", color='#94A3B8', fontsize=13, transform=ax.transAxes)
        
        # Embed screenshot thumbnail cleanly
        thumb = mpimg.imread(os.path.join(IMG_DIR, "dashboard_executive_overview.png"))
        ax_img = fig.add_axes([0.08, 0.20, 0.84, 0.33])
        ax_img.imshow(thumb)
        ax_img.axis('off')
        for spine in ax_img.spines.values():
            spine.set_color('#38BDF8')
            spine.set_linewidth(2)
            
        ax.text(0.08, 0.11, "SWIPE TO SEE ARCHITECTURE & CODE ->", color='#10B981', fontsize=12, fontweight='bold', transform=ax.transAxes)
        ax.text(0.08, 0.06, "By Dwarak6  •  SQL | Python | Power BI | DAX", color='#64748B', fontsize=10, transform=ax.transAxes)
    elif img_embed:
        ax.text(0.08, 0.85, title, color='#FFFFFF', fontsize=20, fontweight='bold', transform=ax.transAxes, va='top')
        ax.text(0.08, 0.77, subtitle, color='#94A3B8', fontsize=12, transform=ax.transAxes)
        
        thumb = mpimg.imread(os.path.join(IMG_DIR, img_embed))
        ax_img = fig.add_axes([0.08, 0.24, 0.84, 0.48])
        ax_img.imshow(thumb)
        ax_img.axis('off')
        
        ax.text(0.08, 0.15, bullets_or_box, color='#CBD5E1', fontsize=11, transform=ax.transAxes,
                bbox=dict(boxstyle='round,pad=0.8', facecolor='#1E293B', edgecolor='#334155', linewidth=1.2))
        ax.text(0.08, 0.06, "Swipe for next slide ->", color='#94A3B8', fontsize=10.5, transform=ax.transAxes)
    else:
        ax.text(0.08, 0.84, title, color='#FFFFFF', fontsize=22, fontweight='bold', transform=ax.transAxes, va='top')
        ax.text(0.08, 0.76, subtitle, color='#94A3B8', fontsize=12.5, transform=ax.transAxes)
        
        # Content Box
        ax.text(0.08, 0.26, bullets_or_box, color='#E2E8F0', fontsize=11.5, transform=ax.transAxes, va='bottom',
                bbox=dict(boxstyle='round,pad=1.0', facecolor='#1E293B', edgecolor='#38BDF8', linewidth=1.5))
        ax.text(0.08, 0.06, "Swipe for next slide ->", color='#94A3B8', fontsize=10.5, transform=ax.transAxes)

    path = os.path.join(TEMP_SLIDES_DIR, f"carousel_s{slide_num}.png")
    plt.savefig(path, dpi=125, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    return path

def generate_linkedin_carousel_pdf():
    print("Building LinkedIn Carousel slides...")
    
    s1 = make_carousel_slide(1, "", "", "", is_cover=True)
    
    s2 = make_carousel_slide(
        2,
        "The High Stakes of\nPayment Fraud",
        "Why standard rule engines fall short in 2025",
        "CORE INDUSTRY CHALLENGES:\n\n"
        "• Global Exposure: Global payment fraud losses surpass\n"
        "  $38 Billion annually. Every INR 1 lost costs INR 3.50+\n"
        "  in dispute management, scheme fines, and churn.\n\n"
        "• The User Friction Dilemma: Blocking every flagged\n"
        "  transaction destroys checkout conversion for honest\n"
        "  customers (INR 150+ friction cost per false positive).\n\n"
        "• Regulatory Penalties: Exceeding Visa/Mastercard's\n"
        "  1.0% chargeback ratio triggers severe acquirer fines."
    )
    
    s3 = make_carousel_slide(
        3,
        "Data Architecture:\nStar Schema Design",
        "Structuring 45,000 transactions for Power BI",
        "DATA WAREHOUSE MODELING:\n\n"
        "• 1 Central Fact Table: `fact_transactions`\n"
        "  - TransactionID, Amount, RiskScore, Status, Loss\n\n"
        "• 3 Dimension Tables (1:* Relationships):\n"
        "  - `dim_customer`: Demographics, KYC, Credit Tier\n"
        "  - `dim_merchant`: Category, Risk Tier, 1% Limit\n"
        "  - `dim_date`: Time-intelligence calendar\n\n"
        "Why Star Schema?\n"
        "✓ Maximizes VertiPaq in-memory compression\n"
        "✓ Accelerates DAX calculation speeds\n"
        "✓ Clean filter propagation across visuals"
    )
    
    s4 = make_carousel_slide(
        4,
        "SQL Analytics:\nWindow Functions",
        "Catching rapid-fire velocity attacks in SQL",
        "SQL VELOCITY & CARD TESTING DETECTION:\n\n"
        "Using window functions to detect rapid card bursts:\n"
        "```sql\n"
        "LAG(Amount, 1) OVER (\n"
        "  PARTITION BY CustomerID, PaymentMethod\n"
        "  ORDER BY TransactionTimestamp\n"
        ") AS Prev_Amount\n"
        "```\n\n"
        "Key Finding:\n"
        "Fraudsters run micro-charges (< INR 150) to verify\n"
        "card validity, followed immediately by high-ticket\n"
        "charges (> INR 25,000) within 10-15 minutes."
    )
    
    s5 = make_carousel_slide(
        5,
        "Machine Learning &\nFinancial ROI",
        "Balanced Random Forest Classifier (0.73 ROC-AUC)",
        "COST-MATRIX OPTIMIZATION & BUSINESS VALUE:\n\n"
        "• Top 3 Predictive Drivers:\n"
        "  1. Masked IP / VPN Proxy: 19.7% weight\n"
        "  2. Ticket Size Anomaly: 17.1% weight\n"
        "  3. Nocturnal Window (00:00 - 05:00): 8.6% weight\n\n"
        "• Net Prevention Impact:\n"
        "  - Gross Fraud Loss Prevented: INR 2.25 Cr\n"
        "  - False Positive Friction Cost: INR 2.48 Lakh\n"
        "  ------------------------------------------------\n"
        "  - NET FINANCIAL BENEFIT: INR 2.23 Cr"
    )
    
    s6 = make_carousel_slide(
        6,
        "Executive Power BI\nDashboard Suite",
        "Interactive governance & merchant monitoring",
        "Features 30+ production DAX measures:\n"
        "Moving Averages, Incurred Loss, and the 1.0% chargeback breach line.",
        img_embed="dashboard_merchant_deepdive.png"
    )
    
    s7 = make_carousel_slide(
        7,
        "Summary &\nKey Takeaways",
        "What this portfolio project demonstrates",
        "KEY TAKEAWAYS:\n\n"
        "✓ End-to-end data pipeline from raw data to BI\n"
        "✓ Advanced SQL CTEs and analytical window functions\n"
        "✓ Machine learning risk scoring tied to business ROI\n"
        "✓ Executive Power BI dashboard with 30+ DAX formulas\n\n"
        "FULL CODE & DATASETS ON GITHUB:\n"
        "https://github.com/Dwarak6/digital-payment-fraud-analytics\n\n"
        "Let's connect and discuss Risk & Data Analytics!"
    )
    
    slides = [Image.open(s).convert('RGB') for s in [s1, s2, s3, s4, s5, s6, s7]]
    pdf_out = os.path.join(DOCS_DIR, "FinGuard_LinkedIn_Carousel_Document.pdf")
    slides[0].save(pdf_out, save_all=True, append_images=slides[1:], resolution=125.0)
    print(f"Flawless LinkedIn Carousel PDF compiled: {pdf_out}")

if __name__ == "__main__":
    generate_executive_report_pdf()
    generate_linkedin_carousel_pdf()
    print("All PDFs successfully generated with zero errors!")

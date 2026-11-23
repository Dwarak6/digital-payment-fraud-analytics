"""
Generate High-Quality Dashboard Visual Mockups & Analytical Charts
Creates ready-to-share visuals for LinkedIn and GitHub README.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACT_PATH = os.path.join(PROJECT_DIR, "data", "processed", "powerbi_fact_transactions.csv")
MERCH_PATH = os.path.join(PROJECT_DIR, "data", "processed", "powerbi_dim_merchants.csv")
CUST_PATH = os.path.join(PROJECT_DIR, "data", "processed", "powerbi_dim_customers.csv")
IMG_DIR = os.path.join(PROJECT_DIR, "images")
os.makedirs(IMG_DIR, exist_ok=True)

# Set high DPI and aesthetic styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#334155'
plt.rcParams['axes.linewidth'] = 0.8

def build_executive_dashboard():
    print("Generating Executive Fraud Overview Dashboard mockup...")
    df = pd.read_csv(FACT_PATH)
    merch = pd.read_csv(MERCH_PATH)
    df = df.merge(merch[["MerchantID", "MerchantCategory"]], on="MerchantID", how="left")
    
    # Aggregates
    total_volume = len(df)
    total_amount = df["Amount"].sum()
    fraud_txs = df[df["IsFraud"] == 1]
    fraud_volume = len(fraud_txs)
    fraud_rate_cnt = (fraud_volume / total_volume) * 100
    total_fraud_loss = df["FraudLossAmount"].sum()
    prevented_loss = df["PreventedLossAmount"].sum()
    chargeback_cnt = len(df[df["ChargebackStatus"].str.contains("Chargeback", na=False)])
    
    fig = plt.figure(figsize=(16, 9), facecolor='#0B0F19')
    
    # Header Banner
    ax_head = fig.add_axes([0.03, 0.90, 0.94, 0.08], facecolor='#1E293B')
    ax_head.text(0.02, 0.60, "FinGuard | Digital Payment Fraud & Risk Analytics Dashboard", color='#FFFFFF', fontsize=18, fontweight='bold')
    ax_head.text(0.02, 0.22, "Executive Overview • FY 2025 • High-Risk Transaction Monitoring & Fraud Prevention", color='#94A3B8', fontsize=11)
    ax_head.text(0.82, 0.40, "Status: LIVE MONITORING", color='#10B981', fontsize=11, fontweight='bold', bbox=dict(boxstyle='round,pad=0.5', facecolor='#064E3B', edgecolor='#10B981'))
    ax_head.axis('off')
    
    # 4 KPI Cards
    kpis = [
        ("Total Processed Volume", f"INR {total_amount/1e7:,.2f} Cr", f"{total_volume:,} Transactions", "#3B82F6"),
        ("Fraud Incurred Loss", f"INR {total_fraud_loss/1e7:,.2f} Cr", f"{fraud_volume:,} Incidents ({fraud_rate_cnt:.2f}%)", "#EF4444"),
        ("Prevented Fraud Loss", f"INR {prevented_loss/1e7:,.2f} Cr", "Automated Rule Engine Hits", "#10B981"),
        ("Chargeback Disputes", f"{chargeback_cnt:,}", f"{(chargeback_cnt/total_volume)*100:.2f}% Dispute Ratio", "#F59E0B")
    ]
    
    card_width = 0.22
    card_spacing = 0.02
    card_y = 0.76
    card_height = 0.11
    
    for i, (title, val, sub, col) in enumerate(kpis):
        cx = 0.03 + i * (card_width + card_spacing)
        ax_card = fig.add_axes([cx, card_y, card_width, card_height], facecolor='#1E293B')
        for spine in ax_card.spines.values():
            spine.set_color(col)
            spine.set_linewidth(1.5)
        ax_card.text(0.08, 0.72, title.upper(), color='#94A3B8', fontsize=9, fontweight='bold')
        ax_card.text(0.08, 0.38, val, color='#FFFFFF', fontsize=16, fontweight='bold')
        ax_card.text(0.08, 0.14, sub, color=col, fontsize=9, fontweight='medium')
        ax_card.set_xticks([])
        ax_card.set_yticks([])
        
    # Chart 1: Monthly Fraud vs Total Volume Trend (Area / Line)
    ax1 = fig.add_axes([0.03, 0.38, 0.58, 0.33], facecolor='#1E293B')
    df["Month"] = pd.to_datetime(df["TransactionDate"]).dt.strftime("%b")
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_tx = df.groupby("Month").agg({"Amount": "sum", "FraudLossAmount": "sum"}).reindex(month_order)
    
    x = np.arange(len(month_order))
    ax1.plot(x, monthly_tx["Amount"] / 1e6, color='#3B82F6', marker='o', linewidth=2.5, label='Total Volume (INR M)')
    ax1.plot(x, monthly_tx["FraudLossAmount"] / 1e6, color='#EF4444', marker='s', linewidth=2.5, label='Fraud Loss (INR M)')
    ax1.fill_between(x, monthly_tx["FraudLossAmount"] / 1e6, color='#EF4444', alpha=0.2)
    ax1.set_xticks(x)
    ax1.set_xticklabels(month_order, color='#94A3B8', fontsize=10)
    ax1.tick_params(colors='#94A3B8')
    ax1.set_title("Monthly Payment Volume vs Incurred Fraud Loss (INR Millions)", color='#FFFFFF', fontsize=12, fontweight='bold', pad=12)
    ax1.grid(True, linestyle='--', alpha=0.15, color='#CBD5E1')
    ax1.legend(loc='upper right', facecolor='#0B0F19', edgecolor='#334155', labelcolor='#FFFFFF')
    
    # Chart 2: Fraud Rate by Payment Method (Horizontal Bar)
    ax2 = fig.add_axes([0.65, 0.38, 0.32, 0.33], facecolor='#1E293B')
    pay_fraud = df.groupby("PaymentMethod").agg(
        Total=('TransactionID', 'count'),
        Fraud=('IsFraud', 'sum')
    )
    pay_fraud["FraudRate"] = (pay_fraud["Fraud"] / pay_fraud["Total"]) * 100
    pay_fraud = pay_fraud.sort_values("FraudRate", ascending=True)
    
    bars = ax2.barh(pay_fraud.index, pay_fraud["FraudRate"], color=['#10B981', '#3B82F6', '#8B5CF6', '#F59E0B', '#EF4444'], height=0.55)
    for bar in bars:
        w = bar.get_width()
        ax2.text(w + 0.3, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", color='#FFFFFF', va='center', fontsize=9, fontweight='bold')
    ax2.set_xlim(0, max(pay_fraud["FraudRate"]) * 1.25)
    ax2.set_title("Fraud Attack Rate by Payment Channel", color='#FFFFFF', fontsize=12, fontweight='bold', pad=12)
    ax2.tick_params(colors='#94A3B8')
    ax2.grid(True, linestyle='--', alpha=0.15, color='#CBD5E1', axis='x')
    
    # Chart 3: Fraud Loss by Merchant Category (Bar chart)
    ax3 = fig.add_axes([0.03, 0.06, 0.58, 0.26], facecolor='#1E293B')
    cat_loss = df.groupby("MerchantCategory")["FraudLossAmount"].sum().sort_values(ascending=False).head(7)
    bars3 = ax3.bar(range(len(cat_loss)), cat_loss / 1e6, color='#6366F1', width=0.55)
    ax3.set_xticks(range(len(cat_loss)))
    ax3.set_xticklabels([c.replace(" ", "\n") for c in cat_loss.index], color='#94A3B8', fontsize=8.5)
    for bar in bars3:
        h = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2, h + 0.3, f"{h:.1f}M", ha='center', color='#FFFFFF', fontsize=8.5, fontweight='bold')
    ax3.set_title("Top 7 Merchant Categories by Net Fraud Loss (INR M)", color='#FFFFFF', fontsize=11, fontweight='bold', pad=10)
    ax3.tick_params(colors='#94A3B8')
    ax3.grid(True, linestyle='--', alpha=0.15, color='#CBD5E1', axis='y')
    
    # Chart 4: Fraud Type Breakdown (Donut Chart)
    ax4 = fig.add_axes([0.65, 0.06, 0.32, 0.26], facecolor='#1E293B')
    fraud_only = df[df["FraudType"] != "None"]
    type_counts = fraud_only["FraudType"].value_counts()
    colors = ['#EF4444', '#F59E0B', '#3B82F6', '#10B981', '#EC4899']
    
    wedges, texts, autotexts = ax4.pie(
        type_counts.values,
        labels=type_counts.index,
        autopct='%1.1f%%',
        colors=colors,
        startangle=140,
        pctdistance=0.75,
        textprops=dict(color='#CBD5E1', fontsize=8.5),
        wedgeprops=dict(width=0.45, edgecolor='#0B0F19')
    )
    for autotext in autotexts:
        autotext.set_color('#FFFFFF')
        autotext.set_fontweight('bold')
    ax4.set_title("Fraud Attack Vector Distribution", color='#FFFFFF', fontsize=11, fontweight='bold', pad=10)
    
    out_path = os.path.join(IMG_DIR, "dashboard_executive_overview.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f"Executive Dashboard saved to: {out_path}")

def build_merchant_deepdive_dashboard():
    print("Generating Merchant Risk & Chargeback Analysis Dashboard mockup...")
    df = pd.read_csv(FACT_PATH)
    merch = pd.read_csv(MERCH_PATH)
    
    m_summary = df.groupby("MerchantID").agg(
        TotalAmount=('Amount', 'sum'),
        TxCount=('TransactionID', 'count'),
        FraudTxCount=('IsFraud', 'sum'),
        FraudAmount=('FraudLossAmount', 'sum'),
        ChargebackCount=('ChargebackStatus', lambda x: x.str.contains('Chargeback').sum())
    ).reset_index()
    
    m_summary = m_summary.merge(merch, on="MerchantID", how="left")
    m_summary["ChargebackRatePct"] = (m_summary["ChargebackCount"] / m_summary["TxCount"]) * 100
    m_summary["FraudRatePct"] = (m_summary["FraudTxCount"] / m_summary["TxCount"]) * 100
    
    fig = plt.figure(figsize=(16, 9), facecolor='#0B0F19')
    
    # Header Banner
    ax_head = fig.add_axes([0.03, 0.90, 0.94, 0.08], facecolor='#1E293B')
    ax_head.text(0.02, 0.60, "FinGuard | Merchant Risk, Chargebacks & Velocity Monitoring", color='#FFFFFF', fontsize=18, fontweight='bold')
    ax_head.text(0.02, 0.22, "Merchant Portfolio Intelligence • Chargeback Ratio Breaches • Acquirer Loss Containment", color='#94A3B8', fontsize=11)
    ax_head.text(0.80, 0.40, "THRESHOLD: 1.0% CBK LIMIT", color='#F59E0B', fontsize=10, fontweight='bold', bbox=dict(boxstyle='round,pad=0.5', facecolor='#78350F', edgecolor='#F59E0B'))
    ax_head.axis('off')
    
    # Scatter Plot: Transaction Count vs Chargeback Rate with Risk Quadrants
    ax1 = fig.add_axes([0.03, 0.10, 0.55, 0.74], facecolor='#1E293B')
    
    colors = []
    for r in m_summary["RiskTier"]:
        if r == "Critical": colors.append('#EF4444')
        elif r in ["High", "Medium-High"]: colors.append('#F59E0B')
        else: colors.append('#3B82F6')
        
    scatter = ax1.scatter(
        m_summary["TxCount"],
        m_summary["ChargebackRatePct"],
        s=m_summary["FraudAmount"] / 80000,
        c=colors,
        alpha=0.75,
        edgecolors='#FFFFFF',
        linewidth=0.5
    )
    
    ax1.axhline(1.0, color='#EF4444', linestyle='--', linewidth=1.5, label='Visa/Mastercard 1% Penalty Threshold')
    ax1.text(m_summary["TxCount"].min() + 10, 1.05, "REGULATORY CHARGEBACK LIMIT (1.0%)", color='#EF4444', fontsize=9, fontweight='bold')
    ax1.set_xlabel("Merchant Transaction Volume (Count)", color='#94A3B8', fontsize=10, fontweight='bold')
    ax1.set_ylabel("Chargeback Dispute Rate (%)", color='#94A3B8', fontsize=10, fontweight='bold')
    ax1.set_title("Merchant Risk Matrix: Transaction Volume vs Chargeback % (Bubble Size = Fraud INR Loss)", color='#FFFFFF', fontsize=12, fontweight='bold', pad=12)
    ax1.tick_params(colors='#94A3B8')
    ax1.grid(True, linestyle='--', alpha=0.15, color='#CBD5E1')
    ax1.legend(loc='upper right', facecolor='#0B0F19', edgecolor='#334155', labelcolor='#FFFFFF')
    
    # Top 8 High Risk Merchants Table (Right panel)
    ax2 = fig.add_axes([0.61, 0.10, 0.36, 0.74], facecolor='#1E293B')
    ax2.set_title("Top High-Risk Merchants Requiring Action / Escrow Hold", color='#FFFFFF', fontsize=12, fontweight='bold', pad=12)
    
    top_violators = m_summary.sort_values("FraudAmount", ascending=False).head(9)
    
    # Custom Table Visualization
    col_labels = ["Merchant", "Category", "Fraud Loss", "CBK %", "Risk Tier"]
    cell_text = []
    for _, row in top_violators.iterrows():
        cell_text.append([
            row["MerchantName"][:13],
            row["MerchantCategory"][:12],
            f"INR {row['FraudAmount']/1e5:.1f}L",
            f"{row['ChargebackRatePct']:.1f}%",
            row["RiskTier"]
        ])
        
    table = ax2.table(
        cellText=cell_text,
        colLabels=col_labels,
        loc='center',
        cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.0, 2.2)
    
    for (i, j), cell in table.get_celld().items():
        cell.set_edgecolor('#334155')
        if i == 0:
            cell.set_facecolor('#0F172A')
            cell.set_text_props(color='#38BDF8', fontweight='bold')
        else:
            cell.set_facecolor('#1E293B' if i % 2 == 0 else '#162032')
            cell.set_text_props(color='#E2E8F0')
            if j == 3 and float(cell_text[i-1][3].replace('%', '')) >= 1.0:
                cell.set_text_props(color='#EF4444', fontweight='bold')
                
    ax2.axis('off')
    
    out_path = os.path.join(IMG_DIR, "dashboard_merchant_deepdive.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f"Merchant Dashboard saved to: {out_path}")

def build_trend_and_hourly_analysis():
    print("Generating Hourly Velocity & Anomaly Chart...")
    df = pd.read_csv(FACT_PATH)
    
    hourly = df.groupby("TransactionHour").agg(
        TotalCount=('TransactionID', 'count'),
        FraudCount=('IsFraud', 'sum')
    )
    hourly["FraudRate"] = (hourly["FraudCount"] / hourly["TotalCount"]) * 100
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), facecolor='#0B0F19')
    for ax in [ax1, ax2]:
        ax.set_facecolor('#1E293B')
        
    # Hourly Velocity
    hours = np.arange(24)
    ax1.bar(hours, hourly["FraudRate"], color='#EF4444', alpha=0.85, width=0.7)
    ax1.set_xticks(hours[::2])
    ax1.set_xticklabels([f"{h:02d}:00" for h in hours[::2]], color='#94A3B8')
    ax1.set_title("Hourly Fraud Attack Concentration (% of Volume)", color='#FFFFFF', fontsize=11, fontweight='bold', pad=10)
    ax1.set_ylabel("Fraud Rate (%)", color='#94A3B8')
    ax1.tick_params(colors='#94A3B8')
    ax1.grid(True, linestyle='--', alpha=0.15, color='#CBD5E1', axis='y')
    ax1.axvspan(0, 4.5, color='#DC2626', alpha=0.15, label='High-Risk Night Window (00:00 - 05:00)')
    ax1.legend(facecolor='#0B0F19', edgecolor='#334155', labelcolor='#FFFFFF')
    
    # Device vs Geo Attack Matrix
    vpn_cross = pd.crosstab(df["DeviceType"], df["IsVPNorProxy"], values=df["IsFraud"], aggfunc='mean') * 100
    devices = vpn_cross.index
    y_pos = np.arange(len(devices))
    
    ax2.barh(y_pos - 0.18, vpn_cross[0], height=0.35, label='Domestic Residential IP', color='#3B82F6')
    ax2.barh(y_pos + 0.18, vpn_cross[1], height=0.35, label='VPN / Anonymizer / Foreign Proxy', color='#F59E0B')
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(devices, color='#94A3B8', fontsize=9.5)
    ax2.set_title("Fraud Propensity by Device & IP Masking", color='#FFFFFF', fontsize=11, fontweight='bold', pad=10)
    ax2.set_xlabel("Fraud Rate (%)", color='#94A3B8')
    ax2.tick_params(colors='#94A3B8')
    ax2.grid(True, linestyle='--', alpha=0.15, color='#CBD5E1', axis='x')
    ax2.legend(facecolor='#0B0F19', edgecolor='#334155', labelcolor='#FFFFFF')
    
    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fraud_trend_analysis.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f"Hourly & Device Analysis saved to: {out_path}")

if __name__ == "__main__":
    build_executive_dashboard()
    build_merchant_deepdive_dashboard()
    build_trend_and_hourly_analysis()
    print("All visual assets successfully generated in images/ directory!")

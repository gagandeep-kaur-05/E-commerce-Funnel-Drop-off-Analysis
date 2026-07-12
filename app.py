"""
app.py — E-Commerce Funnel Drop-off Analysis Dashboard (Premium UI)
Run: streamlit run app.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Funnel Intelligence · GK Analytics",
    page_icon="📉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Premium CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Base reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0A0C10;
    color: #E2E8F0;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0F1117 !important;
    border-right: 1px solid #1E2433;
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label {
    color: #94A3B8 !important;
    font-size: 12px !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 600;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] {
    background: #161B26 !important;
    border: 1px solid #2D3748 !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] {
    margin-top: 8px;
}

/* ── Main content area padding ── */
.block-container {
    padding: 2rem 2.5rem 2rem 2.5rem !important;
    max-width: 1400px;
}

/* ── Page header ── */
.page-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #1E2433;
}
.page-title {
    font-size: 26px;
    font-weight: 700;
    color: #F1F5F9;
    letter-spacing: -0.5px;
    margin: 0;
}
.page-subtitle {
    font-size: 13px;
    color: #64748B;
    margin: 4px 0 0;
    font-weight: 400;
}
.page-badge {
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
    color: white;
    font-size: 11px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ── KPI cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    margin-bottom: 1.5rem;
}
.kpi-card {
    background: #0F1117;
    border: 1px solid #1E2433;
    border-radius: 12px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent);
    border-radius: 12px 12px 0 0;
}
.kpi-label {
    font-size: 11px;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 10px;
}
.kpi-value {
    font-size: 28px;
    font-weight: 700;
    color: #F1F5F9;
    line-height: 1;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 6px;
}
.kpi-delta {
    font-size: 12px;
    font-weight: 500;
    padding: 2px 8px;
    border-radius: 20px;
    display: inline-block;
}
.kpi-delta.good { background: #0F291E; color: #34D399; }
.kpi-delta.bad  { background: #2D1010; color: #F87171; }
.kpi-delta.neutral { background: #1A2035; color: #94A3B8; }

/* ── Section headers ── */
.section-header {
    font-size: 13px;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 0 0 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1E2433;
}

/* ── Chart containers ── */
.chart-card {
    background: #0F1117;
    border: 1px solid #1E2433;
    border-radius: 12px;
    padding: 20px 22px;
    margin-bottom: 14px;
}
.chart-title {
    font-size: 14px;
    font-weight: 600;
    color: #CBD5E1;
    margin-bottom: 4px;
}
.chart-desc {
    font-size: 12px;
    color: #475569;
    margin-bottom: 16px;
}

/* ── Recommendation cards ── */
.rec-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-top: 8px;
}
.rec-card {
    background: #0F1117;
    border: 1px solid #1E2433;
    border-radius: 12px;
    padding: 20px;
    border-left: 3px solid var(--rec-color);
}
.rec-priority {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--rec-color);
    margin-bottom: 8px;
}
.rec-title {
    font-size: 14px;
    font-weight: 600;
    color: #E2E8F0;
    margin-bottom: 10px;
}
.rec-body {
    font-size: 13px;
    color: #64748B;
    line-height: 1.6;
}

/* ── Funnel bars (custom HTML) ── */
.funnel-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 10px;
}
.funnel-stage {
    font-size: 12px;
    color: #94A3B8;
    width: 160px;
    flex-shrink: 0;
    font-weight: 500;
}
.funnel-bar-wrap {
    flex: 1;
    height: 32px;
    background: #161B26;
    border-radius: 6px;
    overflow: hidden;
    position: relative;
}
.funnel-bar-fill {
    height: 100%;
    border-radius: 6px;
    display: flex;
    align-items: center;
    padding-left: 12px;
    font-size: 12px;
    font-weight: 600;
    color: white;
    font-family: 'JetBrains Mono', monospace;
    transition: width 0.6s ease;
}
.funnel-pct {
    font-size: 12px;
    color: #475569;
    width: 48px;
    text-align: right;
    font-family: 'JetBrains Mono', monospace;
    flex-shrink: 0;
}
.funnel-drop {
    font-size: 11px;
    color: #F87171;
    width: 80px;
    text-align: right;
    flex-shrink: 0;
}

/* ── Override default streamlit metric ── */
[data-testid="metric-container"] { display: none; }

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid #1E2433;
    margin: 1.5rem 0;
}

/* ── Footer ── */
.dash-footer {
    text-align: center;
    font-size: 11px;
    color: #334155;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid #1E2433;
    letter-spacing: 0.05em;
}
</style>
""", unsafe_allow_html=True)

# ── Matplotlib dark theme ─────────────────────────────────────────────────────
CHART_BG   = "#0F1117"
GRID_COLOR = "#1E2433"
TEXT_COLOR = "#64748B"
TICK_COLOR = "#475569"

plt.rcParams.update({
    "figure.facecolor":  CHART_BG,
    "axes.facecolor":    CHART_BG,
    "axes.edgecolor":    GRID_COLOR,
    "axes.labelcolor":   TEXT_COLOR,
    "axes.titlecolor":   "#CBD5E1",
    "xtick.color":       TICK_COLOR,
    "ytick.color":       TICK_COLOR,
    "grid.color":        GRID_COLOR,
    "grid.linewidth":    0.6,
    "text.color":        TEXT_COLOR,
    "figure.dpi":        130,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.spines.left":  False,
    "axes.spines.bottom":False,
    "font.family":       "sans-serif",
})

PALETTE = {
    "indigo":  "#6366F1",
    "emerald": "#10B981",
    "red":     "#F87171",
    "amber":   "#FBBF24",
    "purple":  "#A78BFA",
    "blue":    "#60A5FA",
    "slate":   "#64748B",
}

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/orders.csv", parse_dates=["order_date"])
    return df

df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙ FILTERS")
    st.markdown("---")

    all_categories = sorted(df["category"].unique().tolist())
    sel_cat = st.multiselect("Product Category", all_categories, default=all_categories)

    all_payments = sorted(df["payment_method"].unique().tolist())
    sel_pay = st.multiselect("Payment Method", all_payments, default=all_payments)

    all_states = sorted(df["customer_state"].unique().tolist())
    sel_state = st.multiselect("Customer State", all_states, default=all_states)

    min_val, max_val = int(df["order_value_inr"].min()), int(df["order_value_inr"].max())
    val_range = st.slider("Order Value (₹)", min_val, max_val, (min_val, max_val))

    st.markdown("---")
    st.markdown(
        "<p style='font-size:11px;color:#334155;'>GK Analytics · Anurag University<br>B.Tech CSE (Data Science)</p>",
        unsafe_allow_html=True
    )

# ── Filter ────────────────────────────────────────────────────────────────────
dff = df[
    df["category"].isin(sel_cat) &
    df["payment_method"].isin(sel_pay) &
    df["customer_state"].isin(sel_state) &
    df["order_value_inr"].between(*val_range)
].copy()

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<h1 id="page title"; style="color: #6366F1;">GK Analytics</h1>
<div class="page-header">
  <div>
    <p class="page-title", style="font-size: 22px; color: #60A5FA;">Funnel Drop-off Intelligence</p>
    <p class="page-subtitle">E-Commerce Revenue Leak Analysis · 1,10,000 Orders · Prices in INR</p>
  </div>
  <span class="page-badge">Live Dashboard</span>
</div>
""", unsafe_allow_html=True)

# ── KPI cards ─────────────────────────────────────────────────────────────────
total     = len(dff)
approved  = int(dff["payment_approved"].sum())
delivered = int(dff["order_delivered"].sum())
gmv       = dff["order_value_inr"].sum()
rev_del   = dff.loc[dff["order_delivered"], "order_value_inr"].sum()
rev_lost  = gmv - rev_del
conv_rate = delivered / total * 100 if total else 0

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card" style="--accent:#6366F1">
    <div class="kpi-label">Orders Placed</div>
    <div class="kpi-value">{total:,}</div>
    <span class="kpi-delta neutral">Total Volume</span>
  </div>
  <div class="kpi-card" style="--accent:#10B981">
    <div class="kpi-label">Payment Approved</div>
    <div class="kpi-value">{approved:,}</div>
    <span class="kpi-delta good">↑ {approved/total*100:.1f}%</span>
  </div>
  <div class="kpi-card" style="--accent:#60A5FA">
    <div class="kpi-label">Orders Delivered</div>
    <div class="kpi-value">{delivered:,}</div>
    <span class="kpi-delta good">↑ {conv_rate:.1f}%</span>
  </div>
  <div class="kpi-card" style="--accent:#A78BFA">
    <div class="kpi-label">Gross Merch. Value</div>
    <div class="kpi-value">₹{gmv/1e7:.1f}Cr</div>
    <span class="kpi-delta neutral">Placed Orders</span>
  </div>
  <div class="kpi-card" style="--accent:#F87171">
    <div class="kpi-label">Est. Revenue Lost</div>
    <div class="kpi-value">₹{rev_lost/1e7:.1f}Cr</div>
    <span class="kpi-delta bad">↓ {rev_lost/gmv*100:.1f}% of GMV</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Row 1: Funnel + Revenue loss ──────────────────────────────────────────────
st.markdown('<p class="section-header">Purchase Funnel</p>', unsafe_allow_html=True)
col_a, col_b = st.columns([1.1, 0.9])

with col_a:
    stage_labels = ["Order Placed", "Payment Initiated", "Payment Approved", "Order Delivered", "Review Submitted"]
    stage_cols   = [None, "payment_initiated", "payment_approved", "order_delivered", "review_submitted"]
    counts = [total] + [int(dff[c].sum()) for c in stage_cols[1:]]
    colors_funnel = [PALETTE["indigo"], PALETTE["blue"], PALETTE["emerald"], PALETTE["purple"], PALETTE["amber"]]

    funnel_html = '<div class="chart-card"><div class="chart-title">Order Volume by Stage</div><div class="chart-desc">% relative to orders placed</div>'
    for i, (label, cnt, color) in enumerate(zip(stage_labels, counts, colors_funnel)):
        pct_bar = cnt / counts[0] * 100
        pct_txt = f"{pct_bar:.1f}%"
        drop = ""
        if i > 0:
            dropped = counts[i-1] - cnt
            drop = f"−{dropped:,}" if dropped > 0 else ""
        funnel_html += f"""
        <div class="funnel-row">
          <span class="funnel-stage">{label}</span>
          <div class="funnel-bar-wrap">
            <div class="funnel-bar-fill" style="width:{pct_bar:.1f}%;background:linear-gradient(90deg,{color}CC,{color}66)">
              {cnt:,}
            </div>
          </div>
          <span class="funnel-pct">{pct_txt}</span>
          <span class="funnel-drop">{drop}</span>
        </div>"""
    funnel_html += "</div>"
    st.markdown(funnel_html, unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="chart-card"><div class="chart-title">Revenue Lost by Stage</div><div class="chart-desc">Estimated INR value at point of drop-off</div>', unsafe_allow_html=True)

    rev_stages = [dff["order_value_inr"].sum()] + [
        dff.loc[dff[c], "order_value_inr"].sum() for c in stage_cols[1:]]
    lost_labels = stage_labels[1:]
    lost_vals   = [abs(rev_stages[i] - rev_stages[i-1]) / 1e7 for i in range(1, len(rev_stages))]
    bar_colors  = [PALETTE["red"], PALETTE["amber"], PALETTE["purple"], PALETTE["slate"]]

    fig, ax = plt.subplots(figsize=(6, 4.2))
    fig.patch.set_facecolor(CHART_BG)
    bars = ax.bar(lost_labels, lost_vals, color=bar_colors, width=0.55, zorder=3)
    ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.6, zorder=0)
    ax.set_facecolor(CHART_BG)
    for bar, val in zip(bars, lost_vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(lost_vals)*0.03,
                f"₹{val:.1f}Cr", ha="center", fontsize=10, fontweight="600", color="#CBD5E1")
    ax.set_ylabel("₹ Crore", fontsize=11, color=TEXT_COLOR)
    ax.set_ylim(0, max(lost_vals) * 1.3)
    ax.set_xticklabels(lost_labels, rotation=20, ha="right", fontsize=9, color=TICK_COLOR)
    ax.tick_params(colors=TICK_COLOR)
    plt.tight_layout(pad=0.5)
    st.pyplot(fig, use_container_width=True)
    plt.close()
    st.markdown("</div>", unsafe_allow_html=True)

# ── Row 2: Payment + Category ─────────────────────────────────────────────────
st.markdown('<p class="section-header">Segment Breakdown</p>', unsafe_allow_html=True)
col_c, col_d = st.columns(2)

with col_c:
    pay_df = dff.groupby("payment_method").agg(
        total=("order_id","count"),
        approved=("payment_approved","sum")
    ).reset_index()
    pay_df["rate"] = (pay_df["approved"] / pay_df["total"] * 100).round(1)
    pay_df = pay_df.sort_values("rate")

    st.markdown('<div class="chart-card"><div class="chart-title">Payment Approval Rate</div><div class="chart-desc">Lower approval = higher revenue leak</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6, 3.4))
    fig.patch.set_facecolor(CHART_BG)
    grad_colors = [PALETTE["red"] if r < 80 else PALETTE["amber"] if r < 88 else PALETTE["emerald"]
                   for r in pay_df["rate"]]
    bars = ax.barh(pay_df["payment_method"], pay_df["rate"], color=grad_colors, height=0.45, zorder=3)
    ax.xaxis.grid(True, color=GRID_COLOR, linewidth=0.6, zorder=0)
    ax.set_facecolor(CHART_BG)
    for bar, v in zip(bars, pay_df["rate"]):
        ax.text(v + 0.4, bar.get_y() + bar.get_height()/2,
                f"{v}%", va="center", fontsize=10, fontweight="600", color="#CBD5E1")
    ax.set_xlim(0, 108)
    ax.set_xlabel("Approval Rate (%)", fontsize=10, color=TEXT_COLOR)
    ax.tick_params(colors=TICK_COLOR)
    plt.tight_layout(pad=0.5)
    st.pyplot(fig, use_container_width=True)
    plt.close()
    st.markdown("</div>", unsafe_allow_html=True)

with col_d:
    cat_df = dff.groupby("category").agg(
        rev_total=("order_value_inr","sum"),
        rev_delivered=("order_value_inr", lambda x: x[dff.loc[x.index,"order_delivered"]].sum())
    ).reset_index()
    cat_df["lost_cr"] = ((cat_df["rev_total"] - cat_df["rev_delivered"]) / 1e7).round(2)
    cat_df = cat_df.sort_values("lost_cr", ascending=False)

    st.markdown('<div class="chart-card"><div class="chart-title">Revenue Lost by Category</div><div class="chart-desc">Ordered by estimated ₹ loss</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6, 3.4))
    fig.patch.set_facecolor(CHART_BG)
    n = len(cat_df)
    bar_cols = [PALETTE["red"]] + [PALETTE["amber"]] * 2 + [PALETTE["blue"]] * (n - 3)
    bars = ax.bar(cat_df["category"], cat_df["lost_cr"], color=bar_cols, width=0.6, zorder=3)
    ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.6, zorder=0)
    ax.set_facecolor(CHART_BG)
    ax.set_ylabel("₹ Crore", fontsize=10, color=TEXT_COLOR)
    ax.set_xticklabels(cat_df["category"], rotation=35, ha="right", fontsize=8, color=TICK_COLOR)
    ax.tick_params(colors=TICK_COLOR)
    plt.tight_layout(pad=0.5)
    st.pyplot(fig, use_container_width=True)
    plt.close()
    st.markdown("</div>", unsafe_allow_html=True)

# ── Monthly trend ─────────────────────────────────────────────────────────────
st.markdown('<p class="section-header">Trend Analysis</p>', unsafe_allow_html=True)
monthly = dff.groupby("month").agg(
    orders=("order_id","count"), approved=("payment_approved","sum")).reset_index()
monthly["rate"] = (monthly["approved"] / monthly["orders"] * 100).round(1)

st.markdown('<div class="chart-card"><div class="chart-title">Monthly Payment Approval Rate</div><div class="chart-desc">Dips indicate seasonal or operational issues worth investigating</div>', unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(13, 3.2))
fig.patch.set_facecolor(CHART_BG)
ax.plot(monthly["month"], monthly["rate"], marker="o", linewidth=2.5,
        color=PALETTE["indigo"], markersize=5, markerfacecolor="white",
        markeredgecolor=PALETTE["indigo"], markeredgewidth=2, zorder=3)
ax.fill_between(monthly["month"], monthly["rate"], alpha=0.08, color=PALETTE["indigo"])
ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.6, zorder=0)
ax.set_facecolor(CHART_BG)
ax.set_ylabel("Approval Rate (%)", fontsize=10, color=TEXT_COLOR)
ax.set_ylim(70, 100)
ax.set_xticklabels(monthly["month"], rotation=45, ha="right", fontsize=8, color=TICK_COLOR)
ax.tick_params(colors=TICK_COLOR)
plt.tight_layout(pad=0.5)
st.pyplot(fig, use_container_width=True)
plt.close()
st.markdown("</div>", unsafe_allow_html=True)

# ── Recommendations ───────────────────────────────────────────────────────────
st.markdown('<p class="section-header">Business Recommendations</p>', unsafe_allow_html=True)
st.markdown(f"""
<div class="rec-grid">
  <div class="rec-card" style="--rec-color:#F87171">
    <div class="rec-priority" style="font-size: 16px; font-weight: 1000;">
      🔴 Priority 1 — Highest Impact
    </div>
    <div class="rec-title">Fix Payment Approval Leakage</div>
    <div class="rec-body">
      Boleto and voucher payments fail at 22–28% vs 9% for credit cards.
      Surface UPI/credit card options prominently. Add real-time retry suggestions
      and EMI options on high-value carts to recover the largest share of lost revenue.
    </div>
  </div>
  <div class="rec-card" style="--rec-color:#FBBF24">
    <div class="rec-priority" style="font-size: 16px; font-weight: 1000;">
      🟠 Priority 2 — Logistics
    </div>
    <div class="rec-title">Reduce Remote Delivery Failures</div>
    <div class="rec-body">
      Non-metro states show ~6% lower delivery success rates.
      Partner with regional last-mile logistics providers and implement
      proactive WhatsApp/SMS delivery tracking to reduce failed first attempts.
    </div>
  </div>
  <div class="rec-card" style="--rec-color:#60A5FA">
    <div class="rec-priority" style="font-size: 16px; font-weight: 1000;">
      🟡 Priority 3 — Category-Specific
    </div>
    <div class="rec-title">Recover Electronics Drop-offs</div>
    <div class="rec-body">
      Electronics loses the most revenue per dropped order due to high AOV.
      Implement cart-save email recovery flows and display trust signals
      (returns policy, warranty badges) at checkout to reduce hesitation.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-footer">
  Built by Gagandeep Kaur &nbsp;·&nbsp; B.Tech CSE (Data Science) &nbsp;·&nbsp; Anurag University, Hyderabad
</div>
""", unsafe_allow_html=True)

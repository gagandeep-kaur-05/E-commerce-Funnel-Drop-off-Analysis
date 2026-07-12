# E-Commerce Funnel Drop-off Analysis

**Author:** Gagandeep Kaur | B.Tech CSE (Data Science), Anurag University  
**Tools:** Python, Pandas, Matplotlib, Seaborn, Streamlit  
**Dataset:** Synthetic Olist-style dataset — 1,10,000 orders | Prices in INR  

🔗 [Live Dashboard](#) | 📓 [Notebook](notebooks/funnel_analysis.ipynb)

---

## Business Problem

An e-commerce platform processes thousands of orders daily. Not every order placed results in a completed delivery — each drop-off represents lost revenue. This analysis answers:

- **Where** in the purchase funnel are customers dropping off?
- **How much revenue** is lost at each stage?
- **Why** are drop-offs happening (payment method, category, region)?
- **What should the business do** to recover revenue?

---

## Funnel Stages Analysed

```
Order Placed → Payment Initiated → Payment Approved → Order Delivered → Review Submitted
```

---

## Key Findings

| Metric | Value |
|---|---|
| Total Orders Placed | 1,10,000 |
| Orders Successfully Delivered | 88,760 (80.7%) |
| Total Estimated Revenue Lost | ₹3.6 Cr |
| Biggest Single Drop-off Stage | **Payment Approval** |
| Worst Performing Payment Method | Boleto (72% approval) |
| Highest Revenue Loss Category | Electronics |

### 1. Payment Approval is the biggest leak
~14,700 orders (~13%) fail at the payment approval stage. Boleto and voucher payments fail at 22–28% compared to 9% for credit cards. This is the single highest-ROI stage to improve.

### 2. Remote states have lower delivery rates
States outside the top 6 metros show 6% lower delivery success — likely due to last-mile logistics gaps.

### 3. Electronics loses the most revenue per dropped order
High average order values mean even small drop-off rates translate to large revenue loss in electronics.

---

## Business Recommendations

**🔴 Priority 1 — Fix Payment Approval**  
Surface credit card and UPI options more prominently. Add real-time retry suggestions and EMI options to reduce failures on alternative payment methods.

**🟠 Priority 2 — Reduce Remote Delivery Failures**  
Partner with regional last-mile logistics. Add proactive delivery tracking via WhatsApp/SMS to reduce failed first-attempt deliveries.

**🟡 Priority 3 — Recover Electronics Drop-offs**  
Implement cart-save + email recovery for electronics. Display trust signals (returns, warranty) at checkout to reduce hesitation.

---

## Project Structure

```
ecommerce_funnel/
├── data/
│   └── orders.csv              # Generated dataset (110k orders)
├── notebooks/
│   └── funnel_analysis.ipynb   # Full EDA + analysis with markdown commentary
├── app.py                      # Streamlit dashboard (interactive filters)
├── generate_data.py            # Dataset generation script
└── README.md
```

---

## How to Run

```bash
# 1. Clone the repo
git clone https://github.com/gagandeep-kaur-05/ecommerce-funnel-analysis
cd ecommerce-funnel-analysis

# 2. Install dependencies
pip install pandas numpy matplotlib seaborn streamlit

# 3. Generate the dataset
python generate_data.py

# 4. Run the Streamlit dashboard
streamlit run app.py

# 5. Or open the notebook
jupyter notebook notebooks/funnel_analysis.ipynb
```

---

## Resume Bullet Points

> *"Performed funnel drop-off analysis on 1,10,000 e-commerce orders; identified payment approval stage as the primary revenue leak, with Boleto payments failing at 28% — quantified ₹3.6 Cr estimated revenue lost and delivered prioritised business recommendations."*

> *"Built an interactive Streamlit dashboard with dynamic filters (category, payment method, state, order value) enabling segment-level exploration of funnel metrics and revenue loss."*

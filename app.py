import streamlit as st
import plotly.express as px
from utils.data import load_transactions, ensure_demo_data
from utils.config import MODEL_FILE
from utils.ui import page_header

st.set_page_config(page_title="FraudShield AI", page_icon="🛡️", layout="wide")
ensure_demo_data()
df = load_transactions()

st.markdown("""
<style>
    .stApp { background: #081326; color: #f2f6ff; }
    [data-testid="stMetric"] { background: #122440; padding: 16px; border-radius: 12px; border: 1px solid #24466f; }
    section[data-testid="stSidebar"] { background: #0c1c34; }
    div[data-testid="stDataFrame"] { border: 1px solid #24466f; }
</style>
""", unsafe_allow_html=True)

page_header("🛡️ FraudShield AI", "AI-powered transaction fraud monitoring demonstration")
st.info("Demo environment: all included transactions are synthetic. This is a prototype, not a production banking security system.")

total = len(df)
fraud_count = int(df["is_fraud"].sum()) if "is_fraud" in df else 0
fraud_rate = (fraud_count / total * 100) if total else 0
amount = float(df["amount"].sum()) if total else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total transactions", f"{total:,}")
c2.metric("Flagged examples", f"{fraud_count:,}")
c3.metric("Synthetic fraud rate", f"{fraud_rate:.2f}%")
c4.metric("Transaction volume", f"${amount:,.0f}")

left, right = st.columns([1.5, 1])
with left:
    st.subheader("Transaction activity")
    chart = df.copy()
    chart["hour"] = chart["hour"].astype(int)
    by_hour = chart.groupby("hour", as_index=False).agg(
        transactions=("transaction_id", "count"),
        flagged=("is_fraud", "sum")
    )
    fig = px.line(by_hour, x="hour", y=["transactions", "flagged"],
                  markers=True, title="Transactions by hour")
    fig.update_layout(template="plotly_dark", paper_bgcolor="#081326", plot_bgcolor="#081326")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Risk distribution")
    risk_df = df.assign(risk_group=df["is_fraud"].map({0: "Not flagged", 1: "Flagged"}))
    counts = risk_df["risk_group"].value_counts().rename_axis("category").reset_index(name="count")
    fig2 = px.pie(counts, names="category", values="count", hole=0.55,
                  title="Synthetic labels")
    fig2.update_layout(template="plotly_dark", paper_bgcolor="#081326")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Latest transactions")
display_cols = ["transaction_id", "customer_id", "amount", "location", "hour", "status", "is_fraud"]
st.dataframe(df[display_cols].tail(12).sort_index(ascending=False), use_container_width=True, hide_index=True)

st.caption(f"Model file: {'Available' if MODEL_FILE.exists() else 'Not trained yet'}. Use the Fraud Detection page to train the demonstration model.")

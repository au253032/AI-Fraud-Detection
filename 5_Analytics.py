import streamlit as st
import plotly.express as px
from utils.data import load_transactions
from utils.model import load_model

st.set_page_config(page_title="Analytics | FraudShield", page_icon="📈", layout="wide")
st.title("📈 Analytics & Reports")
df = load_transactions()

c1, c2, c3 = st.columns(3)
c1.metric("Total amount", f"${df['amount'].sum():,.2f}")
c2.metric("Average amount", f"${df['amount'].mean():,.2f}")
c3.metric("Flagged examples", f"{int(df['is_fraud'].sum()):,}")

daily = df.groupby("hour", as_index=False).agg(
    transaction_count=("transaction_id", "count"),
    flagged_count=("is_fraud", "sum")
)
fig = px.bar(daily, x="hour", y=["transaction_count","flagged_count"],
             barmode="group", title="Transaction activity by hour")
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

bundle = load_model()
st.subheader("Model performance")
if bundle:
    m = bundle["metrics"]
    st.metric("Test ROC-AUC", f"{m['roc_auc']:.3f}")
    st.write("Confusion matrix (rows: actual class 0/1; columns: predicted class 0/1)")
    st.write(m["confusion_matrix"])
    st.json(m["report"])
else:
    st.info("No model trained yet. Visit Fraud Detection and train the demo model.")

st.download_button("Download analytics source data", df.to_csv(index=False).encode("utf-8"),
                   file_name="fraudshield_analytics_data.csv", mime="text/csv")

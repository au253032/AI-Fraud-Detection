import streamlit as st
import pandas as pd
from utils.model import train_demo_model, load_model, predict_one
from utils.config import FEATURES
from utils.ui import risk_label, risk_color

st.set_page_config(page_title="Fraud Detection | FraudShield", page_icon="🔎", layout="wide")
st.title("🔎 AI Fraud Detection")
st.caption("Train a model on synthetic data and score a sample transaction.")

with st.expander("1. Train or refresh the demonstration model", expanded=True):
    st.warning("Training data is generated synthetically for this demo. Do not use this model to make real banking decisions.")
    if st.button("Train demonstration model", type="primary"):
        with st.spinner("Training Random Forest model..."):
            metrics = train_demo_model()
        st.success(f"Model trained. Test ROC-AUC: {metrics['roc_auc']:.3f}")

bundle = load_model()
if bundle is None:
    st.info("Train the model above before scoring a transaction.")
    st.stop()

st.subheader("2. Enter transaction details")
with st.form("transaction_form"):
    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("Transaction amount", min_value=0.01, value=8500.0, step=50.0)
        hour = st.slider("Hour of day", 0, 23, 2)
        new_device = st.selectbox("New device?", ["No", "Yes"])
        location_mismatch = st.selectbox("Unusual location?", ["No", "Yes"])
    with col2:
        tx_count = st.number_input("Transactions in last hour", min_value=0, max_value=30, value=5)
        ratio = st.number_input("Amount / customer's usual average", min_value=0.1, max_value=50.0, value=8.0)
        failed_logins = st.number_input("Recent failed logins", min_value=0, max_value=20, value=2)
    submitted = st.form_submit_button("Analyze transaction", type="primary")

if submitted:
    row = {
        "amount": amount, "hour": hour,
        "is_new_device": int(new_device == "Yes"),
        "location_mismatch": int(location_mismatch == "Yes"),
        "tx_count_1h": tx_count, "avg_amount_ratio": ratio,
        "failed_logins": failed_logins,
    }
    score = predict_one(bundle, row)
    st.divider()
    st.subheader("AI assessment")
    st.metric("Estimated fraud probability", f"{score*100:.1f}%")
    st.progress(score)
    st.write(f"Risk category: **{risk_color(score)} {risk_label(score)}**")
    if score >= 0.70:
        st.error("Suggested demo action: hold for human investigation.")
    elif score >= 0.35:
        st.warning("Suggested demo action: request additional verification.")
    else:
        st.success("Suggested demo action: continue normal checks.")
    reasons = []
    if row["is_new_device"]: reasons.append("New device")
    if row["location_mismatch"]: reasons.append("Unusual location")
    if row["failed_logins"] >= 2: reasons.append("Multiple failed logins")
    if row["avg_amount_ratio"] >= 4: reasons.append("Amount is much higher than usual")
    if row["tx_count_1h"] >= 5: reasons.append("High transaction frequency")
    st.write("Potential risk indicators:", ", ".join(reasons) if reasons else "No obvious indicators in the entered fields.")
    st.caption("The probability is produced by a model trained on synthetic data. It is not validated for real-world use.")

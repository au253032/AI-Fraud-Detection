import streamlit as st
from utils.data import load_transactions

st.set_page_config(page_title="Fraud Alerts | FraudShield", page_icon="🚨", layout="wide")
st.title("🚨 Fraud Alerts")
st.caption("Review records labelled as suspicious in the synthetic demonstration dataset.")
df = load_transactions()
alerts = df[df["is_fraud"] == 1].copy().sort_values("amount", ascending=False)

min_amount = st.number_input("Minimum transaction amount", min_value=0.0, value=0.0, step=100.0)
alerts = alerts[alerts["amount"] >= min_amount]
st.metric("Matching alerts", len(alerts))
if alerts.empty:
    st.success("No matching demo alerts.")
else:
    st.dataframe(alerts[["transaction_id","customer_id","amount","location","hour","is_new_device","location_mismatch","failed_logins"]],
                 use_container_width=True, hide_index=True)
st.warning("These are synthetic labelled examples, not live alerts from a bank.")

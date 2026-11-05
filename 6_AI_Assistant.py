import streamlit as st
from utils.data import load_transactions

st.set_page_config(page_title="AI Assistant | FraudShield", page_icon="🤖", layout="wide")
st.title("🤖 Fraud Investigation Assistant")
st.caption("A rule-based explanatory demo. This page does not connect to an external LLM.")
df = load_transactions()

question = st.text_input("Ask a question", placeholder="For example: show high-value flagged transactions")
if st.button("Get answer") and question.strip():
    q = question.lower()
    if any(word in q for word in ["high", "large", "amount", "value"]):
        result = df[df["is_fraud"] == 1].nlargest(10, "amount")
        st.write("Here are the 10 highest-value synthetic flagged examples:")
        st.dataframe(result[["transaction_id","amount","location","hour"]], use_container_width=True, hide_index=True)
    elif any(word in q for word in ["how many", "count", "total", "fraud"]):
        st.write(f"There are **{int(df['is_fraud'].sum())}** synthetic records labelled as fraud out of **{len(df)}** transactions.")
    elif "location" in q:
        result = df[df["is_fraud"] == 1].groupby("location").size().reset_index(name="flagged examples")
        st.dataframe(result, use_container_width=True, hide_index=True)
    else:
        st.info("Try asking: 'How many fraud examples are there?', 'Show high-value flagged transactions', or 'Which locations have flagged examples?'")

st.divider()
st.subheader("Explain a flagged transaction")
txid = st.text_input("Transaction ID", placeholder="TXN000001")
if st.button("Explain transaction"):
    match = df[df["transaction_id"].astype(str).str.upper() == txid.strip().upper()]
    if match.empty:
        st.error("Transaction ID not found in the demo dataset.")
    else:
        row = match.iloc[0]
        reasons = []
        if row["is_new_device"]: reasons.append("The transaction used a new device.")
        if row["location_mismatch"]: reasons.append("The location differs from the customer's usual location.")
        if row["failed_logins"] >= 2: reasons.append("There were multiple recent failed login attempts.")
        if row["avg_amount_ratio"] >= 4: reasons.append("The amount was much higher than the customer's usual average.")
        if row["tx_count_1h"] >= 5: reasons.append("Transaction frequency was unusually high.")
        st.write(f"**Transaction:** {row['transaction_id']}")
        st.write(f"**Synthetic label:** {'Flagged' if row['is_fraud'] else 'Not flagged'}")
        st.write("**Possible indicators:**")
        st.write(reasons if reasons else ["No listed indicators were triggered."])
        st.caption("This is a simple explanation based on demo fields, not a causal explanation from a validated banking model.")

import streamlit as st
from utils.data import load_transactions

st.set_page_config(page_title="Transactions | FraudShield", page_icon="💳", layout="wide")
st.title("💳 Transactions")
st.caption("Search and filter the synthetic transaction dataset.")
df = load_transactions()

query = st.text_input("Search transaction or customer ID")
status = st.selectbox("Status", ["All", "Approved", "Flagged"])
min_amount = st.number_input("Minimum amount", min_value=0.0, value=0.0, step=10.0)

view = df.copy()
if query:
    mask = view["transaction_id"].astype(str).str.contains(query, case=False) | view["customer_id"].astype(str).str.contains(query, case=False)
    view = view[mask]
if status != "All":
    view = view[view["status"] == status]
view = view[view["amount"] >= min_amount]

st.write(f"Showing {len(view)} transactions")
st.dataframe(view.sort_values("amount", ascending=False), use_container_width=True, hide_index=True)
st.download_button("Download filtered CSV", view.to_csv(index=False).encode("utf-8"),
                   file_name="fraudshield_transactions.csv", mime="text/csv")

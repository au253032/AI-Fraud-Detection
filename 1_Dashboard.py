import streamlit as st
import plotly.express as px
from utils.data import load_transactions
from utils.ui import page_header

st.set_page_config(page_title="Dashboard | FraudShield", page_icon="📊", layout="wide")
page_header("📊 Dashboard", "Overview of synthetic transaction activity")
df = load_transactions()

a, b, c = st.columns(3)
a.metric("Transactions", f"{len(df):,}")
b.metric("Flagged", f"{int(df['is_fraud'].sum()):,}")
c.metric("Flag rate", f"{df['is_fraud'].mean()*100:.2f}%")

st.subheader("Flagged transactions by location")
loc = df.groupby("location", as_index=False)["is_fraud"].sum().rename(columns={"is_fraud":"flagged"})
fig = px.bar(loc, x="location", y="flagged", color="flagged", title="Synthetic flagged examples by location")
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Amount distribution")
fig2 = px.histogram(df, x="amount", color="is_fraud", nbins=40, barmode="overlay",
                    labels={"is_fraud":"Synthetic fraud label"})
fig2.update_layout(template="plotly_dark")
st.plotly_chart(fig2, use_container_width=True)

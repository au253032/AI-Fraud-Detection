# FraudShield AI

A Streamlit-based educational prototype for AI-assisted transaction fraud detection.

## Important limitations
- The included data is synthetic and generated locally.
- The model is trained on synthetic labels and is not suitable for real banking decisions.
- The AI Assistant is a rule-based demo, not a connected large language model.
- Do not upload real customer, card, account, or banking information.
- Before any real-world pilot, obtain authorization, complete security/privacy reviews, validate models on representative data, and add human review and audit controls.

## Run on Windows CMD

```cmd
cd /d C:\Users\RC\Downloads\FraudShieldAI
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown by Streamlit, usually http://localhost:8501.

## First use
1. Open the Fraud Detection page.
2. Click **Train demonstration model**.
3. Enter transaction details and click **Analyze transaction**.
4. Explore Transactions, Fraud Alerts, Analytics, and AI Assistant.

## Files
- `app.py`: home page
- `pages/`: Streamlit pages
- `utils/`: data generation, model training, configuration, UI helpers
- `data/`: generated demo transactions
- `models/`: trained model is saved here after training

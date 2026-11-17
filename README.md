# FinAssist — Smart Banking Chatbot

A local educational prototype based on the FinAssist project described in the training report.

## Features
- Demo login with three fictional customers
- Dashboard with simulated balance and account details
- Natural-language intent matching for balance, transactions, ATM locations, loans, account opening and human support
- SQLite storage for sample customers, transactions and support requests
- Banking FAQ section
- Streamlit chat interface

## Requirements
- Python 3.9+
- Packages in `requirements.txt`

## Run on Windows
1. Extract the ZIP.
2. Open the extracted `FinAssist` folder in VS Code.
3. Open Terminal in that folder.
4. Run:

```bash
py -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
streamlit run app.py
```

If `py` is unavailable, use `python` instead.

Streamlit will open the app in your browser, usually at http://localhost:8501.

## Demo credentials
- Customer ID: `1001`, PIN: `1234`
- Customer ID: `1002`, PIN: `2345`
- Customer ID: `1003`, PIN: `3456`

## Important scope note
This is a working classroom prototype. It uses a rule-based intent matcher and fictional SQLite records. It is not connected to IBM watsonx, a real bank, payment rails, live ATM services, or a real generative AI model. The report describes IBM watsonx Assistant as the intended enterprise platform; this prototype demonstrates the same core banking conversation flows locally.

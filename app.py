import streamlit as st
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).with_name("finassist.db")

st.set_page_config(page_title="FinAssist | Smart Banking", page_icon="🏦", layout="wide")

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY, name TEXT, pin TEXT, account_type TEXT,
            balance REAL, account_number TEXT)""")
        cur.execute("""CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id TEXT, date TEXT,
            description TEXT, amount REAL, kind TEXT)""")
        cur.execute("""CREATE TABLE IF NOT EXISTS support_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id TEXT, message TEXT,
            created_at TEXT, status TEXT)""")
        count = cur.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        if count == 0:
            customers = [
                ("1001", "Aarav Sharma", "1234", "Savings", 52450.75, "XXXX-XXXX-1024"),
                ("1002", "Priya Verma", "2345", "Current", 81720.00, "XXXX-XXXX-2048"),
                ("1003", "Rahul Mehta", "3456", "Savings", 12680.50, "XXXX-XXXX-3096"),
            ]
            cur.executemany("INSERT INTO customers VALUES (?,?,?,?,?,?)", customers)
            tx = [
                ("1001","2026-11-16","Salary credit",35000,"Credit"),
                ("1001","2026-11-15","Grocery store",-1850,"Debit"),
                ("1001","2026-11-13","Electricity bill",-1240,"Debit"),
                ("1001","2026-11-10","Online transfer",-2500,"Debit"),
                ("1002","2026-11-16","Client payment",22000,"Credit"),
                ("1002","2026-11-14","Office supplies",-4200,"Debit"),
                ("1003","2026-11-15","UPI payment",-650,"Debit"),
            ]
            cur.executemany("INSERT INTO transactions (customer_id,date,description,amount,kind) VALUES (?,?,?,?,?)", tx)
        con.commit()

def customer(cid):
    with get_conn() as con:
        row = con.execute("SELECT customer_id,name,pin,account_type,balance,account_number FROM customers WHERE customer_id=?", (cid,)).fetchone()
    return row

def transactions(cid):
    with get_conn() as con:
        rows = con.execute("SELECT date,description,amount,kind FROM transactions WHERE customer_id=? ORDER BY date DESC,id DESC LIMIT 10", (cid,)).fetchall()
    return rows

def save_support(cid, message):
    with get_conn() as con:
        con.execute("INSERT INTO support_requests(customer_id,message,created_at,status) VALUES(?,?,?,?)",
                    (cid, message, datetime.now().strftime("%Y-%m-%d %H:%M"), "Open"))
        con.commit()

def respond(message, user):
    q = message.lower()
    if any(x in q for x in ["balance", "how much money", "available amount"]):
        return f"Your available **{user[3]} account balance** is **₹{user[4]:,.2f}**. This is sample demonstration data."
    if any(x in q for x in ["transaction", "statement", "payment history", "recent payments"]):
        rows = transactions(user[0])
        if not rows:
            return "There are no transactions available in this demo account."
        lines = [f"- {d}: {desc} — {'+' if amt >= 0 else ''}₹{amt:,.2f} ({kind})" for d,desc,amt,kind in rows]
        return "Here are your latest transactions:\n" + "\n".join(lines)
    if any(x in q for x in ["atm", "cash machine", "cash withdrawal", "branch"]):
        return ("Here are sample ATM/branch locations for this demo:\n"
                "- Connaught Place, New Delhi — 24-hour ATM\n"
                "- Kashmere Gate, Delhi — ATM and branch\n"
                "- Laxmi Nagar, Delhi — ATM\n\n"
                "These are illustrative locations, not live availability data.")
    if any(x in q for x in ["loan", "borrow", "emi", "home loan", "personal loan"]):
        return ("I can guide you through a loan application. Typical steps are:\n"
                "1. Choose a loan type (personal, home, or education).\n"
                "2. Check eligibility and required documents.\n"
                "3. Submit an application to the bank.\n"
                "4. The bank verifies your details and communicates its decision.\n\n"
                "This demo does not approve loans or calculate an official interest rate.")
    if any(x in q for x in ["open account", "new account", "create account"]):
        return ("To open a bank account, generally:\n"
                "1. Choose savings or current account.\n"
                "2. Complete the bank's application form.\n"
                "3. Submit valid KYC documents as requested by the bank.\n"
                "4. Complete verification. Account opening is not performed in this demo.")
    if any(x in q for x in ["lost card", "stolen card", "fraud", "unauthorized", "block card", "human", "agent", "support"]):
        return ("This request needs human assistance. Please contact your bank using the official number on its website or your card. "
                "For this demo, use the **Raise support request** option in the sidebar. Do not share your PIN, OTP, or full card number here.")
    if any(x in q for x in ["hello", "hi", "hey"]):
        return f"Hello {user[1]}! I'm FinAssist. I can help with balances, transactions, ATMs, loans and banking FAQs."
    return ("I can help with these topics:\n"
            "- Check my balance\n- Show recent transactions\n- Find an ATM\n"
            "- How do I apply for a loan?\n- How do I open a bank account?\n"
            "- I need human support\n\nPlease try asking one of these in your own words.")

init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("""
<style>
.main {background-color:#f5f8fc;}
.block-container {padding-top:1.6rem; max-width:1200px;}
.hero {background:linear-gradient(110deg,#102b55,#1769aa);padding:26px;border-radius:18px;color:white;}
.hero h1 {color:white;margin:0;font-size:2.1rem;}
.hero p {color:#e3efff;margin:7px 0 0 0;}
div[data-testid="stMetric"] {background:white;padding:16px;border:1px solid #e5ebf3;border-radius:14px;}
.stChatMessage {border-radius:12px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🏦 FinAssist</h1><p>Your smart banking companion · Simple, secure and available 24/7</p></div>', unsafe_allow_html=True)
st.write("")

if not st.session_state.logged_in:
    left, center, right = st.columns([1,1.2,1])
    with center:
        st.subheader("Welcome to digital banking")
        st.write("Sign in with a demo customer account to explore FinAssist.")
        cid = st.text_input("Customer ID", value="1001")
        pin = st.text_input("Demo PIN", value="1234", type="password")
        if st.button("Sign in", type="primary", use_container_width=True):
            user = customer(cid.strip())
            if user and user[2] == pin:
                st.session_state.logged_in = True
                st.session_state.customer_id = cid.strip()
                st.session_state.messages = [{"role":"assistant","content":f"Welcome {user[1]}! I'm FinAssist. Ask me about your balance, transactions, ATMs or loans."}]
                st.rerun()
            else:
                st.error("Invalid demo Customer ID or PIN.")
        st.info("Demo credentials: ID 1001 / PIN 1234 · ID 1002 / PIN 2345 · ID 1003 / PIN 3456")
    st.caption("Educational prototype only. Uses fictional sample banking data; not connected to a real bank.")
    st.stop()

user = customer(st.session_state.customer_id)
with st.sidebar:
    st.title("FinAssist Menu")
    st.success(f"Signed in as {user[1]}")
    st.caption(f"Customer ID: {user[0]}")
    pages = ["Dashboard", "AI Banking Assistant", "Transactions", "Banking FAQs"]
    default_page = st.session_state.pop("page_to_open", "Dashboard")
    page = st.radio("Navigate", pages, index=pages.index(default_page) if default_page in pages else 0)
    st.divider()
    st.subheader("Human support")
    support_text = st.text_area("Describe your issue", placeholder="I need help with...")
    if st.button("Raise support request", use_container_width=True):
        if support_text.strip():
            save_support(user[0], support_text.strip())
            st.success("Demo support request saved.")
        else:
            st.warning("Please describe your issue first.")
    if st.button("Log out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.messages = []
        st.rerun()

if page == "Dashboard":
    st.subheader(f"Good day, {user[1]} 👋")
    st.write("Here's a quick overview of your demo account.")
    a,b,c = st.columns(3)
    a.metric("Available balance", f"₹{user[4]:,.2f}")
    b.metric("Account type", user[3])
    c.metric("Account number", user[5])
    st.subheader("Quick actions")
    q1,q2,q3,q4 = st.columns(4)
    if q1.button("💰 Check balance", use_container_width=True):
        st.session_state.quick_prompt = "Check my balance"
        st.session_state.page_to_open = "AI Banking Assistant"
        st.rerun()
    if q2.button("🧾 Transactions", use_container_width=True):
        st.session_state.page_to_open = "Transactions"
        st.rerun()
    if q3.button("🏧 Find ATM", use_container_width=True):
        st.session_state.quick_prompt = "Find an ATM near me"
        st.session_state.page_to_open = "AI Banking Assistant"
        st.rerun()
    if q4.button("📄 Loan guidance", use_container_width=True):
        st.session_state.quick_prompt = "How can I apply for a loan?"
        st.session_state.page_to_open = "AI Banking Assistant"
        st.rerun()
    st.info("All balances and transactions shown here are fictional demo records.")
elif page == "AI Banking Assistant":
    st.subheader("💬 Chat with FinAssist")
    st.write("Ask a banking question using natural language.")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    prompt = st.chat_input("Example: What is my account balance?")
    if "quick_prompt" in st.session_state:
        prompt = st.session_state.pop("quick_prompt")
    if prompt:
        st.session_state.messages.append({"role":"user","content":prompt})
        answer = respond(prompt, user)
        st.session_state.messages.append({"role":"assistant","content":answer})
        st.rerun()
elif page == "Transactions":
    st.subheader("🧾 Recent transactions")
    rows = transactions(user[0])
    if rows:
        for d,desc,amt,kind in rows:
            col1,col2,col3 = st.columns([2,4,2])
            col1.write(d)
            col2.write(desc)
            col3.markdown(f"**{'+' if amt >= 0 else ''}₹{amt:,.2f}**")
            st.divider()
    else:
        st.info("No transactions found.")
elif page == "Banking FAQs":
    st.subheader("Frequently asked questions")
    faqs = {
        "How can I reset my banking password?":"Use your bank's official app or website and select Forgot Password. Complete the bank's verification steps. Never share an OTP.",
        "What is KYC?":"KYC means Know Your Customer. Banks use it to verify a customer's identity and address.",
        "How do I report an unauthorized transaction?":"Contact your bank immediately through its official app, website or verified helpline and follow its dispute process.",
        "How do I apply for a loan?":"Choose the loan type, check eligibility, prepare required documents and submit an application through the bank's official channel.",
        "How can I find an ATM?":"Use your bank's official ATM locator or ask FinAssist for the sample locations in this demonstration."
    }
    for question, answer in faqs.items():
        with st.expander(question):
            st.write(answer)

st.caption("FinAssist prototype · Simulated data only · Never enter real PINs, OTPs or banking credentials.")

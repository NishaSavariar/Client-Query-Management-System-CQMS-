import streamlit as st
import mysql.connector
import hashlib

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

st.set_page_config(page_title="Login", layout="centered")

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Iniya@08",
        database="cqms_simple",
        autocommit=True
    )

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user and user["password"] == hash_password(password):
        return user
    return None

st.markdown("""
<style>

html, body {
    margin: 0 !important;
    padding: 0 !important;
}

/* NEW Streamlit padding remover */
[data-testid="block-container"] {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* Removes entire top white gap */
[data-testid="stAppViewContainer"] > div:first-child {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* Removes invisible spacer Streamlit adds */
div.block-container {
    padding-top: 0 !important;
}

/* Remove padding on the main wrapper */
section.main {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* Login box styling */
.login-box {
    background: white;
    padding: 30px 35px;
    border-radius: 15px;
    box-shadow: 0 4px 25px rgba(0,0,0,0.15);
    width: 430px;
    margin-left: auto;
    margin-right: auto;
    margin-top: 0 !important;  /* <---- Force it to start at the top */
}

/* Title style */
.title-text {
    font-size: 26px;
    font-weight: bold;
    color: #2d5bd8;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)


st.markdown("<div class='login-box'>", unsafe_allow_html=True)

st.markdown("""
<div class="title-text">
    🔐 Client Query Management System
</div>
""", unsafe_allow_html=True)


username = st.text_input("👤 Username")
password = st.text_input("🔑 Password", type="password")

if st.button("Login"):
    user = login_user(username, password)

    if user:
        st.success("Login Successful! Redirecting...")

        st.session_state["role"] = user["role"]
        st.session_state["logged_in"] = True

        if user["role"].lower() == "client":
            st.switch_page("pages/1_Client.py")
        elif user["role"].lower() == "support":
            st.switch_page("pages/2_Support.py")
    else:
        st.error("Invalid username or password")

st.markdown("</div>", unsafe_allow_html=True)

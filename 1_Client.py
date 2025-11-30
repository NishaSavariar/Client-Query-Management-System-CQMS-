import streamlit as st
from simple_utils import insert_query
import time

st.set_page_config(page_title="Client Page", layout="centered")


if "role" not in st.session_state:
    st.error("Unauthorized! Please login first.")
    st.stop()

if st.session_state["role"].lower() != "client":
    st.error("Access denied! Clients only.")
    st.stop()


def logout():
    st.session_state.clear()
    st.rerun()

st.sidebar.header("Client Menu")
if st.sidebar.button("🚪 Logout"):
    logout()


st.markdown("""
<style>

body {
    background-color: #eef2f7;
}

/* Card container */
.form-card {
    background: white;
    padding: 35px 40px;
    border-radius: 18px;
    box-shadow: 0 6px 30px rgba(0,0,0,0.12);
    width: 500px;
    margin-left: auto;
    margin-right: auto;
    animation: fadeIn 1s ease;
}

/* Fade-in animation */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Gradient title */
.page-title {
    font-size: 30px;
    font-weight: bold;
    text-align: center;
    padding-bottom: 10px;
    background: linear-gradient(90deg, #2341c9, #517cff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Field labels */
label {
    font-size: 16px !important;
    font-weight: 600 !important;
    color: #2a3d66 !important;
}

/* Inputs */
input, textarea {
    border-radius: 10px !important;
}

/* Button */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #2341c9, #517cff) !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 12px 0 !important;
    font-size: 17px !important;
    font-weight: 600 !important;
    border: none;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.stButton > button:hover {
    background: linear-gradient(90deg, #1b32a8, #3c66e6) !important;
}

/* Success animation box */
.success-card {
    background: #e8f7e9;
    border-left: 6px solid #3cb043;
    padding: 15px;
    margin-top: 20px;
    border-radius: 10px;
    font-size: 18px;
    color: #1f6b2e;
    animation: fadeIn 0.8s ease;
}

</style>
""", unsafe_allow_html=True)


st.markdown("<h2 class='page-title'>📝 Submit Your Query</h2>", unsafe_allow_html=True)
st.markdown("<div class='form-card'>", unsafe_allow_html=True)

email = st.text_input("📧 Email")
mobile = st.text_input("📱 Mobile Number")
heading = st.text_input("📝 Query Heading")
description = st.text_area("📄 Query Description", height=140)

submit_btn = st.button("Submit Query")


if submit_btn:
    if email and mobile and heading and description:

        insert_query(email, mobile, heading, description)

        st.balloons()

        st.markdown("""
            <div class='success-card'>
                🎉 <b>Your query has been submitted successfully!</b>
            </div>
        """, unsafe_allow_html=True)

        time.sleep(1)
        st.rerun()

    else:
        st.error("⚠️ Please fill all fields.")

st.markdown("</div>", unsafe_allow_html=True)


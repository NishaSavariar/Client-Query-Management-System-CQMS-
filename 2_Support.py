import streamlit as st
import pandas as pd
from simple_utils import load_all_queries_df
from simple_utils import get_all_queries, close_query_response

st.set_page_config(page_title="Support Dashboard", layout="wide")

if "role" not in st.session_state:
    st.error("Unauthorized! Please login first.")
    st.stop()

if st.session_state["role"].lower() != "support":
    st.error("Access denied! Support only.")
    st.stop()

def logout():
    st.session_state.clear()     
    st.rerun()                  
    
st.sidebar.header("Support Menu")
if st.sidebar.button("Logout"):
    logout()


st.markdown("""
    <h2 style='text-align:center; color:#3B82F6;'>
        🛠️ Support Dashboard
    </h2>
    <p style='text-align:center; color:gray;'>
        Manage client queries, close tickets & respond easily.
    </p>
""", unsafe_allow_html=True)


status = st.selectbox("🔍 Filter by Status", ["All", "Open", "Closed"])

queries = get_all_queries(status)

items_per_page = 5
total_items = len(queries)
total_pages = (total_items - 1) // items_per_page + 1

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    page = st.number_input("📄 Page", min_value=1, max_value=total_pages, value=1)

start = (page - 1) * items_per_page
end = start + items_per_page
page_queries = queries[start:end]

st.write(f"Showing **{len(page_queries)}** of **{total_items}** queries")


def render_status_badge(status):
    color = "#22C55E" if status == "Closed" else "#EF4444"
    return f"""
        <span style="
            background-color:{color};
            padding:6px 12px;
            border-radius:8px;
            color:white;
            font-size:13px;
            font-weight:600;">
            {status}
        </span>
    """

for q in page_queries:
    with st.container():
        st.markdown("""
            <div style="
                border:1px solid #e0e0e0;
                padding:20px;
                margin-bottom:15px;
                border-radius:12px;
                box-shadow:0 2px 5px rgba(0,0,0,0.05);
                background:white;">
        """, unsafe_allow_html=True)


        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"### 📨 Query #{q['query_id']}: {q['query_heading']}")
            st.markdown(f"**📧 Mail:** {q['mail_id']}  \n**📱 Mobile:** {q['mobile_number']}")
            st.markdown(f"**🕒 Created:** {q['query_created_time']}")

        with col2:
            st.markdown(render_status_badge(q["status"]), unsafe_allow_html=True)

        st.divider()

    
        st.markdown(f"**📝 Description:** {q['query_description']}")

        if q["status"] == "Closed":
            st.success(f"💬 Response: {q.get('query_response', '')}")
        else:
            
            response = st.text_area(f"💬 Enter Response for Query {q['query_id']}", key=f"resp_{q['query_id']}")

            if st.button(f"✔ Close Query {q['query_id']}", key=f"close_{q['query_id']}"):
                if response.strip() == "":
                    st.error("⚠ Please enter a response before closing.")
                else:
                    close_query_response(q["query_id"], response)
                    st.success("Query closed successfully!")
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

st.divider()



st.subheader("📊 Query Analytics Dashboard")

df = load_all_queries_df()

st.markdown("### 📈 Monthly Query Trend")

df['query_created_time'] = pd.to_datetime(df['query_created_time'])

df_month = df.groupby(df['query_created_time'].dt.to_period('M')).size()
df_month.index = df_month.index.astype(str)

st.line_chart(df_month)


st.markdown("### ⏱ Average Resolution Time (Closed Queries)")

df_closed = df[df['status'] == 'Closed'].copy()

if len(df_closed) > 0:
    df_closed['query_closed_time'] = pd.to_datetime(df_closed['query_closed_time'])
    df_closed['resolution_hours'] = (
        df_closed['query_closed_time'] - df_closed['query_created_time']
    ).dt.total_seconds() / 3600  # hours

    avg_resolution = df_closed['resolution_hours'].mean()

    st.metric(
        label="Average Resolution Time (hours)",
        value=f"{avg_resolution:.2f} hrs"
    )

    st.bar_chart(df_closed[['resolution_hours']])
else:
    st.info("No closed queries available to calculate resolution time.")


st.markdown("""
    <p style='text-align:center; color:gray; margin-top:20px;'>
        © Client Query Management System
    </p>
""", unsafe_allow_html=True)

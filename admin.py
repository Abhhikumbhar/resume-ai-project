import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="ResumeAI Admin",
    page_icon="📊",
    layout="wide"
)

# ==========================
# CSS
# ==========================

st.markdown("""
<style>

.stApp{
background:linear-gradient(
135deg,
#dff6fb,
#edfafd,
#d8f7ff
);
}

header{
visibility:hidden;
}

footer{
visibility:hidden;
}

.dashboard-title{
font-size:50px;
font-weight:900;
text-align:center;
color:#0f172a;
margin-bottom:20px;
}

.metric-card{
background:white;
padding:25px;
border-radius:25px;
box-shadow:0px 10px 25px rgba(0,0,0,.08);
text-align:center;
}

[data-testid="stSidebar"]{
background:#1f2937;
}

[data-testid="stSidebar"] *{
color:white !important;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# DATABASE
# ==========================

try:

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="resumeai"
    )

    cursor = conn.cursor(
        dictionary=True
    )

except Exception as e:

    st.error(
        f"MySQL Error: {e}"
    )

    st.stop()

# ==========================
# TITLE
# ==========================
import bcrypt

if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

def verify_password(password, hashed):
    return bcrypt.checkpw(
        password.encode(),
        hashed.encode()
    )

if not st.session_state.admin_logged:

    st.markdown("""
    <div style="
    max-width:500px;
    margin:auto;
    background:white;
    padding:40px;
    border-radius:25px;
    box-shadow:0px 10px 30px rgba(0,0,0,.08);
    text-align:center;">
    <h1>🔐 ResumeAI Admin Login</h1>
    </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        cursor.execute(
            """
            SELECT *
            FROM admin
            WHERE username=%s
            """,
            (username,)
        )

        admin = cursor.fetchone()

        if admin and verify_password(
            password,
            admin["password"]
        ):

            st.session_state.admin_logged = True

            st.success(
                "Login Successful"
            )

            st.rerun()

        else:

            st.error(
                "Invalid Username or Password"
            )

    st.stop()
# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🛡️ ResumeAI Admin")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Users",
        "Activities",
        "Premium Users",
        "Logout"
    ]
)

st.sidebar.markdown("---")

cursor.execute("""
SELECT COUNT(*) total_users
FROM users
""")
users_count = cursor.fetchone()["total_users"]

cursor.execute("""
SELECT COUNT(*) total_analysis
FROM analytics
""")
analysis_count = cursor.fetchone()["total_analysis"]

st.sidebar.info(f"""
👥 Users : {users_count}

📄 Analysis : {analysis_count}

🛡️ Role : Admin
""")

if menu == "Dashboard":

    st.markdown("""
    <div class='dashboard-title'>
    📊 ResumeAI Admin Dashboard
    </div>
    """, unsafe_allow_html=True)

    cursor.execute("SELECT COUNT(*) total_users FROM users")
    total_users = cursor.fetchone()["total_users"]

    cursor.execute("SELECT COUNT(*) total_analysis FROM analytics")
    total_analysis = cursor.fetchone()["total_analysis"]

    cursor.execute("SELECT AVG(resume_score) avg_score FROM analytics")
    avg_score = cursor.fetchone()["avg_score"]

    cursor.execute("SELECT COUNT(*) total_activity FROM history")
    total_activity = cursor.fetchone()["total_activity"]

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric("👥 Users", total_users)

    with col2:
        st.metric("📄 Analysis", total_analysis)

    with col3:
        st.metric("⭐ Avg Score", round(avg_score or 0,2))

    with col4:
        st.metric("📜 Activities", total_activity)

    st.divider()

    st.subheader("Recent Users")

    cursor.execute("""
    SELECT username,role,created_at
    FROM users
    ORDER BY id DESC
    LIMIT 10
    """)

    users = cursor.fetchall()

    if users:
        st.dataframe(
            pd.DataFrame(users),
            use_container_width=True
        )

elif menu == "Users":

    st.title("👥 User Management")

    search = st.text_input(
        "🔍 Search User"
    )

    if search:

        cursor.execute("""
        SELECT id,username,role,created_at
        FROM users
        WHERE username LIKE %s
        """,
        ('%' + search + '%',)
        )

    else:

        cursor.execute("""
        SELECT id,username,role,created_at
        FROM users
        ORDER BY id DESC
        """)

    users = cursor.fetchall()

    if users:

        df = pd.DataFrame(users)

        st.dataframe(
            df,
            use_container_width=True
        )

        st.subheader("Delete User")

        user_id = st.selectbox(
            "Select User ID",
            df["id"].tolist()
        )

        if st.button("Delete User"):

            cursor.execute(
                """
                DELETE FROM users
                WHERE id=%s
                """,
                (user_id,)
            )

            conn.commit()

            st.success(
                "User Deleted Successfully"
            )

            st.rerun()


elif menu == "Activities":
    st.title("📜 User Activities")

    cursor.execute("""
    SELECT username,action_name,created_at
    FROM history
    ORDER BY id DESC
    """)

    activities = cursor.fetchall()

    if activities:

        df = pd.DataFrame(activities)

        st.dataframe(
            df,
            use_container_width=True
        )

        fig = px.histogram(
            df,
            x="action_name",
            title="Activity Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

elif menu == "Premium Users":

    st.title("👑 Premium Subscribers")

    cursor.execute("""
    SELECT *
    FROM premium_subscriptions
    ORDER BY id DESC
    """)

    premium = cursor.fetchall()

    if premium:

        df = pd.DataFrame(premium)

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.warning(
            "No Premium Users Found"
        )

elif menu == "Logout":

    st.session_state.admin_logged = False

    st.success(
        "Logged Out Successfully"
    )

    st.rerun()


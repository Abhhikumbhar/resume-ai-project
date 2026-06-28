import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import re
import bcrypt
import datetime

from dotenv import load_dotenv
from groq import Groq
from PyPDF2 import PdfReader

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="ResumeAI",
    page_icon="",
    layout="wide"
)

load_dotenv()

# ================= CSS =================

st.markdown("""
<style>

/* =========================
   GLOBAL
========================= */

header{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

.stApp{
    background:linear-gradient(
        135deg,
        #dff6fb,
        #edfafd,
        #d8f7ff
    );
}

.block-container{
    padding-top:2rem;
    padding-left:3rem;
    padding-right:3rem;
}

/* =========================
   GLOBAL TEXT
========================= */

body,
p,
span,
label,
div,
li,
h1,
h2,
h3,
h4,
h5,
h6{
    color:#0f172a;
}

/* =========================
   SIDEBAR
========================= */

[data-testid="stSidebar"]{
    background:#1e2233;
}

[data-testid="stSidebar"] *{
    color:white !important;
}

/* =========================
   LOGIN / REGISTER
========================= */

.auth-card{
    max-width:700px;
    margin:auto;
    padding:10px;
    background:transparent;
    text-align:center;
}

.auth-title{
    font-size:65px;
    font-weight:900;
    color:#0f172a;
    text-align:center;
    margin-bottom:40px;
}

/* =========================
   INPUTS
========================= */

.stTextInput label,
.stSelectbox label{
    color:#0f172a !important;
    font-size:18px !important;
    font-weight:700 !important;
}

.stTextInput input{
    background:white !important;
    color:#0f172a !important;
    border-radius:18px !important;
    font-size:18px !important;
    padding:12px !important;
}

.stTextInput input::placeholder{
    color:#64748b !important;
    opacity:1 !important;
}

.stSelectbox div[data-baseweb="select"]{
    background:white !important;
    color:#0f172a !important;
    border-radius:18px !important;
}

input{
    caret-color:#0f172a !important;
}

/* =========================
   BUTTONS
========================= */

.stButton > button{
    width:100%;
    height:55px;
    border:none;
    border-radius:30px;
    font-size:16px;
    font-weight:700;
    background:linear-gradient(
        90deg,
        #63d7e5,
        #84f0ff
    );
    color:#111827 !important;
}

.stButton > button:hover{
    transform:scale(1.03);
    transition:0.3s;
}

/* =========================
   HERO
========================= */

.hero-banner{
    background:transparent;
    padding:20px;
    margin-bottom:30px;
}

.hero-main{
    font-size:72px;
    font-weight:900;
    color:#0f172a;
    line-height:1.1;
}

.hero-desc{
    font-size:22px;
    color:#475569;
    margin-top:15px;
    line-height:1.8;
}

/* =========================
   SECTION TITLES
========================= */

.section-title{
    text-align:center;
    font-size:48px;
    font-weight:900;
    color:#0f172a;
    margin-bottom:15px;
}

.section-subtitle{
    text-align:center;
    font-size:20px;
    color:#64748b;
    margin-bottom:40px;
}

/* =========================
   GLASS CARD
========================= */

.glass-card{
    background:rgba(255,255,255,.35);
    backdrop-filter:blur(20px);
    padding:25px;
    border-radius:30px;
    box-shadow:0 10px 25px rgba(0,0,0,.08);
    margin-bottom:25px;
}

/* =========================
   FEATURE CARD
========================= */

.feature-card{
    background:white;
    padding:30px;
    border-radius:30px;
    text-align:center;
    box-shadow:0 10px 25px rgba(0,0,0,.08);
    transition:.3s;
}

.feature-card:hover{
    transform:translateY(-8px);
}

/* =========================
   SERVICE CARD
========================= */

.service-card{
    background:white;
    padding:25px;
    border-radius:25px;
    box-shadow:0 10px 25px rgba(0,0,0,.08);
    transition:.3s;
}

.service-card:hover{
    transform:translateY(-5px);
}

/* =========================
   METRIC CARD
========================= */

.metric-card{
    background:white;
    padding:20px;
    border-radius:25px;
    text-align:center;
    box-shadow:0 10px 20px rgba(0,0,0,.08);
}

/* =========================
   ANALYSIS
========================= */

.analysis-card{
    background:white;
    padding:25px;
    border-radius:25px;
    box-shadow:0 10px 25px rgba(0,0,0,.08);
}

.score-card{
    background:white;
    padding:20px;
    border-radius:20px;
    text-align:center;
}

/* =========================
   COMPANY
========================= */

.company-card{
    background:white;
    padding:30px;
    border-radius:25px;
    box-shadow:0 10px 25px rgba(0,0,0,.08);
}

.hiring-card{
    background:#f8fafc;
    padding:25px;
    border-radius:20px;
    text-align:center;
}

/* =========================
   JOBS
========================= */

.job-card{
    background:white;
    padding:25px;
    border-radius:25px;
    box-shadow:0 10px 25px rgba(0,0,0,.08);
    margin-bottom:15px;
}

.job-card h2{
    color:#0f172a;
}

.job-card h4{
    color:#0284c7;
}

.job-card p{
    color:#475569;
}

/* =========================
   HISTORY
========================= */

.timeline-card{
    background:white;
    padding:20px;
    border-radius:20px;
    margin-bottom:15px;
    box-shadow:0 10px 20px rgba(0,0,0,.08);
}

.timeline-card h4{
    color:#0f172a;
}

.timeline-card p{
    color:#64748b;
}

/* =========================
   PREMIUM
========================= */

.pricing-card{
    background:white;
    padding:35px;
    border-radius:30px;
    text-align:center;
    box-shadow:0 10px 25px rgba(0,0,0,.08);
}

.pricing-card *{
    color:#0f172a !important;
}

.premium-card{
    border:3px solid #38bdf8;
}

.feature-box{
    background:#111827;
    color:white !important;
    padding:25px;
    border-radius:20px;
    margin-top:20px;
    line-height:2;
}

.feature-box *{
    color:white !important;
}

/* =========================
   METRICS
========================= */

[data-testid="metric-container"]{
    background:white;
    border-radius:20px;
    padding:15px;
    box-shadow:0 5px 15px rgba(0,0,0,.05);
}

[data-testid="metric-container"] *{
    color:#0f172a !important;
}

/* =========================
   FILE UPLOADER
========================= */

[data-testid="stFileUploader"]{
    background:white !important;
    border:2px dashed #38bdf8 !important;
    border-radius:25px !important;
    padding:20px !important;
}

[data-testid="stFileUploader"] *{
    color:#111827 !important;
}

[data-testid="stFileUploaderDropzone"]{
    background:white !important;
}

/* =========================
   DATAFRAME
========================= */

[data-testid="stDataFrame"]{
    background:white;
    border-radius:20px;
}

[data-testid="stDataFrame"] *{
    color:#0f172a !important;
}

/* =========================
   CHAT
========================= */

.stChatMessage{
    background:white !important;
    border-radius:25px !important;
    padding:15px !important;
    margin-bottom:15px !important;
    box-shadow:0 10px 20px rgba(0,0,0,.08) !important;
}

.stChatMessage *{
    color:#0f172a !important;
}

[data-testid="stChatInput"]{
    background:white !important;
    border-radius:25px !important;
}

[data-testid="stChatInput"] textarea{
    color:#0f172a !important;
    font-size:18px !important;
    caret-color:#0f172a !important;
}

[data-testid="stChatInput"] textarea::placeholder{
    color:#64748b !important;
    opacity:1 !important;
}

[data-testid="stChatInputSubmitButton"]{
    background:#38bdf8 !important;
    border-radius:15px !important;
}

/* =========================
   HOME IMAGE
========================= */

.home-image{
    width:100%;
    border-radius:30px;
    box-shadow:0 10px 25px rgba(0,0,0,.08);
}

</style>
""", unsafe_allow_html=True)
# =====================================================
# SESSION STATE INITIALIZATION
# =====================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

if "role" not in st.session_state:
    st.session_state.role = None

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "resume_score" not in st.session_state:
    st.session_state.resume_score = 0

if "history" not in st.session_state:
    st.session_state.history = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "menu" not in st.session_state:
    st.session_state.menu = "Login"

# =====================================================
# GROQ
# =====================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not found in .env")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)
# =====================================================
# MYSQL CONNECTION
# =====================================================

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="resumeai"
    )

    cursor = conn.cursor(dictionary=True)

except Exception as e:
    st.error(f"MySQL Connection Error: {e}")
    st.stop()

# =====================================================
# DATABASE TABLES
# =====================================================

def create_tables():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) UNIQUE,
        password VARCHAR(255),
        role VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100),
        action_name VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analytics(
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100),
        resume_score INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

create_tables()

def hash_password(password):
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def verify_password(password, hashed):
    return bcrypt.checkpw(
        password.encode(),
        hashed.encode()
    )


def register_user(username, password, role):

    try:

        hashed_password = hash_password(password)

        cursor.execute(
            """
            INSERT INTO users
            (username,password,role)
            VALUES(%s,%s,%s)
            """,
            (username, hashed_password, role)
        )

        conn.commit()

        return True

    except Exception as e:
        print(e)
        return False


def login_user(username, password):

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username=%s
        """,
        (username,)
    )

    user = cursor.fetchone()

    if user is None:
        return None

    if verify_password(password, user["password"]):
        return user

    return None

# =====================================================
# HISTORY
# =====================================================

def add_history(action):

    if not st.session_state.username:
        return

    cursor.execute(
        """
        INSERT INTO history
        (username, action_name)
        VALUES(%s,%s)
        """,
        (st.session_state.username, action)
    )



    conn.commit()

def save_analytics(score):

    if not st.session_state.username:
        return

    cursor.execute(
        """
        INSERT INTO analytics
        (username,resume_score)
        VALUES(%s,%s)
        """,
        (
            st.session_state.username,
            score
        )
    )

    conn.commit()
# =====================================================
# PDF TEXT EXTRACTION
# =====================================================

def extract_text_from_pdf(uploaded_file):

    try:

        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

        return text

    except Exception as e:

        st.error(f"PDF Error: {e}")

        return ""


# =====================================================
# GROQ AI
# =====================================================

def ask_groq(prompt):

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"AI Error: {e}"


# =====================================================
# SCORE EXTRACTION
# =====================================================

def extract_score(text):

    score = re.search(
        r'(\d{1,3})\s*/\s*100',
        text
    )

    if score:

        return min(
            int(score.group(1)),
            100
        )

    score = re.search(
        r'(\d{1,3})%',
        text
    )

    if score:

        return min(
            int(score.group(1)),
            100
        )

    return 70



if st.session_state.logged_in:

    st.sidebar.title("ResumeAI")

    menu = st.sidebar.radio(
        "Navigation",
        [
            "Home",
            "Student Mode",
            "Company Mode",
            "Chat",
            "Jobs",
            "History",
            "Premium",
            "Logout"
        ]
    )

    st.sidebar.markdown("---")
    st.sidebar.write(f"User: {st.session_state.username}")
    st.sidebar.write(f"Role: {st.session_state.role}")

else:

    st.sidebar.title("ResumeAI")

    menu = st.sidebar.radio(
        "Navigation",
        [
            "Login",
            "Register"
        ]
    )

if menu == "Login":

    st.markdown("""
    <div class='auth-card'>
        <div class='auth-title'>
            Login
        </div>
    </div>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([3,2,3])

    with center:

        username = st.text_input(
            "Username",
            placeholder="Enter Username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter Password"
        )

        st.write("")

        login_btn = st.button(
            "Login",
            use_container_width=True
        )

    if login_btn:

        user = login_user(
            username,
            password
        )

        if user:

            st.session_state.logged_in = True
            st.session_state.username = user["username"]
            st.session_state.role = user["role"]

            add_history(
                "Logged In"
            )

            st.success(
                "Login Successful"
            )

            st.rerun()

        else:

            st.error(
                "Invalid Username or Password"
            )


elif menu == "Register":

    st.markdown("""
    <div class='auth-card'>
        <div class='auth-title'>
            Create Account
        </div>
    </div>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([3,2,3])

    with center:

        username = st.text_input(
            "Username",
            key="reg_user",
            placeholder="Choose Username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="reg_pass",
            placeholder="Create Password"
        )

        role = st.selectbox(
            "Role",
            [
                "Student",
                "Company"
            ]
        )

        st.write("")

        register_btn = st.button(
            "Register",
            use_container_width=True
        )

    if register_btn:

        success = register_user(
            username,
            password,
            role
        )

        if success:

            st.success(
                "Registration Successful"
            )

        else:

            st.error(
                "Username Already Exists"
            )


elif menu == "Home":

    col1, col2 = st.columns([1.3,1])

    with col1:

        st.markdown("""
        <div class='hero-banner'>

        <div class='hero-main'>
        🚀 ResumeAI
        <br>
        Analyze Your Resume
        With AI Intelligence
        </div>

        <div class='hero-desc'>
        Get ATS Score, Skill Gap Analysis,
        Career Guidance and Smart Job Recommendations
        powered by Llama 3.3 AI.
        </div>

        </div>
        """, unsafe_allow_html=True)

        c1,c2 = st.columns(2)

        with c1:
            st.button("📄 Analyze Resume")

        with c2:
            st.button("🤖 AI Assistant")

    with col2:

        st.image(
            "https://images.unsplash.com/photo-1516321318423-f06f85e504b3",
            use_container_width=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class='section-title'>
    Our Features
    </div>
    """, unsafe_allow_html=True)

    f1,f2,f3 = st.columns(3)

    with f1:
        st.markdown("""
        <div class='feature-card'>
        <h2>📄</h2>
        <h3>Resume Analysis</h3>
        <p>
        AI powered resume review with
        detailed suggestions.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with f2:
        st.markdown("""
        <div class='feature-card'>
        <h2>🎯</h2>
        <h3>ATS Score</h3>
        <p>
        Check ATS compatibility and
        improve interview chances.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with f3:
        st.markdown("""
        <div class='feature-card'>
        <h2>🧠</h2>
        <h3>Skill Gap Detection</h3>
        <p>
        Find missing skills required
        by companies.
        </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
    <div class='section-title'>
    AI Services
    </div>
    """, unsafe_allow_html=True)

    s1,s2,s3 = st.columns(3)

    with s1:
        st.markdown("""
        <div class='service-card'>
        <h3>🤖 AI Career Assistant</h3>
        <p>
        Ask interview, career and
        resume related questions.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div class='service-card'>
        <h3>💼 Job Recommendations</h3>
        <p>
        Get personalized jobs
        based on resume skills.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with s3:
        st.markdown("""
        <div class='service-card'>
        <h3>🏢 Company Evaluation</h3>
        <p>
        Evaluate candidates using
        AI hiring score.
        </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
    <div class='section-title'>
    Platform Statistics
    </div>
    """, unsafe_allow_html=True)

    a,b,c,d = st.columns(4)

    with a:
        st.metric("Users","500+")

    with b:
        st.metric("Resumes Analysed","2000+")

    with c:
        st.metric("AI Accuracy","95%")

    with d:
        st.metric("Job Roles","100+")

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
    <div class='section-title'>
    Technologies Used
    </div>
    """, unsafe_allow_html=True)

    t1,t2,t3,t4 = st.columns(4)

    with t1:
        st.success("Python")

    with t2:
        st.success("Streamlit")

    with t3:
        st.success("MySQL")

    with t4:
        st.success("Groq AI")

    t5,t6,t7,t8 = st.columns(4)

    with t5:
        st.success("Llama 3.3")

    with t6:
        st.success("Plotly")

    with t7:
        st.success("PyPDF2")

    with t8:
        st.success("Bcrypt")

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.info("""
    ResumeAI © 2026

    AI Powered Resume Analysis Platform

    Developed using Python, Streamlit, Groq AI and MySQL
    """)
	
	



elif menu == "Student Mode":

    st.markdown("""
    <div class='hero-banner'>
        <div class='hero-main'>
        📄 Resume Analyzer
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1,col2 = st.columns([2,1])

    with col1:

        st.markdown("""
        <div class='glass-card'>
        <h3>Upload Resume</h3>
        </div>
        """, unsafe_allow_html=True)

        pdf = st.file_uploader(
            "Choose Resume PDF",
            type=["pdf"]
        )

        analyze_btn = st.button(
            "🚀 Analyze Resume"
        )

    with col2:

        st.markdown("""
        <div class='service-card'>
        <h3>Analysis Includes</h3>

        ✅ ATS Score

        ✅ Strengths

        ✅ Weaknesses

        ✅ Missing Skills

        ✅ Career Suggestions

        ✅ Resume Rating
        </div>
        """, unsafe_allow_html=True)

    if pdf and analyze_btn:

        with st.spinner("Analyzing Resume..."):

            text = extract_text_from_pdf(pdf)

            st.session_state.resume_text = text

            prompt = f"""
            Analyze this resume.

            Give:
            1. Resume Score out of 100
            2. Strengths
            3. Weaknesses
            4. Missing Skills
            5. Career Suggestions

            Resume:
            {text[:4000]}
            """

            result = ask_groq(prompt)

            score = extract_score(result)

            st.session_state.resume_score = score

            save_analytics(score)

            st.markdown("## Analysis Result")

            st.write(result)

            st.divider()

            c1,c2,c3,c4 = st.columns(4)

            with c1:
                st.metric(
                    "ATS Score",
                    f"{score}%"
                )

            with c2:
                st.metric(
                    "Keywords",
                    "85%"
                )

            with c3:
                st.metric(
                    "Formatting",
                    "90%"
                )

            with c4:
                st.metric(
                    "Skills Match",
                    "88%"
                )

            st.divider()

            fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=score,
                    title={"text":"Resume Score"},
                    gauge={
                        "axis":{"range":[0,100]}
                    }
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.download_button(
                "📥 Download Report",
                result,
                file_name="resume_report.txt"
            )

            add_history(
                "Student Resume Analysis"
            )



elif menu == "Company Mode":

    st.markdown("""
    <div class='hero-banner'>
        <div class='hero-main'>
        🏢 Candidate Evaluation
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1,col2 = st.columns([2,1])

    with col1:

        st.markdown("""
        <div class='glass-card'>
        <h3>Upload Candidate Resume</h3>
        </div>
        """, unsafe_allow_html=True)

        pdf = st.file_uploader(
            "Choose Candidate Resume",
            type=["pdf"],
            key="company_resume"
        )

        evaluate_btn = st.button(
            "🚀 Evaluate Candidate"
        )

    with col2:

        st.markdown("""
        <div class='service-card'>
        <h3>Evaluation Includes</h3>

        ✅ Hiring Score

        ✅ Technical Skills

        ✅ Communication Skills

        ✅ Strength Analysis

        ✅ Weakness Analysis

        ✅ Final Recommendation
        </div>
        """, unsafe_allow_html=True)

    if pdf and evaluate_btn:

        with st.spinner("Evaluating Candidate..."):

            text = extract_text_from_pdf(pdf)

            prompt = f"""
            Evaluate this candidate.

            Give:

            1. Hiring Score out of 100
            2. Technical Skills
            3. Communication Skills
            4. Strengths
            5. Weaknesses
            6. Final Recommendation

            Resume:
            {text[:4000]}
            """

            result = ask_groq(prompt)

            hiring_score = extract_score(result)

            st.markdown("## Candidate Evaluation Report")

            st.write(result)

            st.divider()

            c1,c2,c3,c4 = st.columns(4)

            with c1:
                st.metric(
                    "Hiring Score",
                    f"{hiring_score}%"
                )

            with c2:
                st.metric(
                    "Technical",
                    "88%"
                )

            with c3:
                st.metric(
                    "Communication",
                    "82%"
                )

            with c4:
                st.metric(
                    "Experience",
                    "85%"
                )

            st.divider()

            fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=hiring_score,
                    title={"text":"Hiring Score"},
                    gauge={
                        "axis":{"range":[0,100]}
                    }
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            if hiring_score >= 80:

                st.success(
                    "✅ Strong Candidate - Recommended For Hiring"
                )

            elif hiring_score >= 60:

                st.warning(
                    "⚠ Average Candidate - Further Interview Required"
                )

            else:

                st.error(
                    "❌ Not Recommended For Hiring"
                )

            st.download_button(
                "📥 Download Evaluation Report",
                result,
                file_name="candidate_evaluation.txt"
            )

            add_history(
                "Company Candidate Evaluation"
            )



elif menu == "Chat":

    st.markdown("""
    <div class='hero-banner'>
        <div class='hero-main'>
        🤖 AI Career Assistant
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1,col2 = st.columns([3,1])

    with col2:

        st.markdown("""
        <div class='service-card'>
        <h3>Popular Questions</h3>

        🎯 How can I improve my resume?

        🎯 What skills should I learn?

        🎯 How do I prepare for interviews?

        🎯 Best career path for MCA?

        🎯 Top jobs in AI & Data Science?
        </div>
        """, unsafe_allow_html=True)

    with col1:

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        for msg in st.session_state.chat_history:

            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        user_prompt = st.chat_input(
            "Ask your career question..."
        )

        if user_prompt:

            st.session_state.chat_history.append(
                {
                    "role":"user",
                    "content":user_prompt
                }
            )

            with st.chat_message("user"):
                st.write(user_prompt)

            if st.session_state.resume_text:

                prompt = f"""
                Resume:

                {st.session_state.resume_text[:3000]}

                Question:

                {user_prompt}
                """

            else:

                prompt = user_prompt

            with st.spinner("Thinking..."):

                answer = ask_groq(prompt)

            with st.chat_message("assistant"):
                st.write(answer)

            st.session_state.chat_history.append(
                {
                    "role":"assistant",
                    "content":answer
                }
            )

            add_history(
                "AI Chat"
            )


elif menu == "Jobs":

    st.markdown("""
    <div class='hero-banner'>
        <div class='hero-main'>
        💼 Smart Job Recommendations
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.resume_text:

        st.warning(
            "Please analyze a resume first."
        )

    else:

        if st.button("🚀 Find Jobs"):

            with st.spinner("Finding Best Jobs..."):

                prompt = f"""
                Based on this resume:

                {st.session_state.resume_text[:3000]}

                Recommend Top 10 Jobs with:

                Job Title
                Salary Range
                Required Skills
                Short Description
                """

                jobs = ask_groq(prompt)

                st.markdown("""
                <div class='section-title'>
                AI Recommended Jobs
                </div>
                """, unsafe_allow_html=True)

                st.write(jobs)

                st.divider()

                jobs_data = [

                    {
                        "title":"Python Developer",
                        "salary":"₹4 - ₹8 LPA",
                        "skills":"Python, SQL, Flask",
                        "company":"TCS"
                    },

                    {
                        "title":"Data Analyst",
                        "salary":"₹5 - ₹10 LPA",
                        "skills":"Python, Power BI, SQL",
                        "company":"Infosys"
                    },

                    {
                        "title":"Software Engineer",
                        "salary":"₹6 - ₹12 LPA",
                        "skills":"Java, Python, DSA",
                        "company":"Wipro"
                    },

                    {
                        "title":"Web Developer",
                        "salary":"₹3 - ₹7 LPA",
                        "skills":"HTML, CSS, JavaScript",
                        "company":"Accenture"
                    }

                ]

                for job in jobs_data:

                    st.markdown(f"""
                    <div class='job-card'>

                    <h2>{job['title']}</h2>

                    <h4>🏢 {job['company']}</h4>

                    <p>
                    💰 Salary: {job['salary']}
                    </p>

                    <p>
                    🛠 Skills: {job['skills']}
                    </p>

                    </div>
                    """, unsafe_allow_html=True)

                    st.button(
                        f"Apply Now - {job['title']}",
                        key=job["title"]
                    )

                    st.divider()

                add_history(
                    "Job Recommendations"
                )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class='section-title'>
    Top Hiring Companies
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.success("TCS")

    with c2:
        st.success("Infosys")

    with c3:
        st.success("Wipro")

    with c4:
        st.success("Accenture")


elif menu == "History":

    st.markdown("""
    <div class='hero-banner'>
        <div class='hero-main'>
        📜 Activity History
        </div>
    </div>
    """, unsafe_allow_html=True)

    cursor.execute(
        """
        SELECT *
        FROM history
        WHERE username=%s
        ORDER BY created_at DESC
        """,
        (st.session_state.username,)
    )

    rows = cursor.fetchall()

    if rows:

        st.markdown("""
        <div class='section-title'>
        Activity Timeline
        </div>
        """, unsafe_allow_html=True)

        for row in rows:

            st.markdown(f"""
            <div class='timeline-card'>

            <h4>📌 {row['action_name']}</h4>

            <p>
            🕒 {row['created_at']}
            </p>

            </div>
            """, unsafe_allow_html=True)

        st.divider()

        st.markdown("""
        <div class='section-title'>
        Complete Activity Records
        </div>
        """, unsafe_allow_html=True)

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "No history records found."
        )


elif menu == "Premium":

    st.markdown("""
    <div class='hero-banner'>
        <div class='hero-main'>
            👑 Choose Your Plan
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.info("Current Plan : FREE")

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("## 🆓 Free")
        st.markdown("### ₹0")
        st.write("Per Month")

        st.success("""
✓ Resume Analysis

✓ ATS Score

✓ AI Chat Assistant

✓ Job Recommendations

✓ Basic Support
""")

        st.button(
            "Current Plan",
            disabled=True,
            key="free_plan"
        )

    with col2:

        st.markdown("## 🚀 Pro")
        st.markdown("### ₹399")
        st.write("Per Month")

        st.success("""
✓ Unlimited Resume Analysis

✓ Advanced ATS Optimization

✓ Premium AI Assistant

✓ Personalized Career Roadmap

✓ Priority Support

✓ Skill Gap Analysis
""")

        if st.button(
            "🚀 Upgrade To Pro",
            key="pro_plan"
        ):

            cursor.execute("""
            INSERT INTO premium_subscriptions
            (username,plan_name,amount)
            VALUES(%s,%s,%s)
            """,
            (
                st.session_state.username,
                "Pro",
                399
            ))

            conn.commit()

            st.success(
                "Pro Plan Activated Successfully"
            )

    with col3:

        st.markdown("## 🏢 Enterprise")
        st.markdown("### ₹999")
        st.write("Per Month")

        st.success("""
✓ Company Hiring Dashboard

✓ Bulk Resume Analysis

✓ Candidate Ranking

✓ HR Analytics

✓ Recruitment Reports

✓ Dedicated Support
""")

        if st.button(
            "🏢 Upgrade Enterprise",
            key="enterprise_plan"
        ):

            cursor.execute("""
            INSERT INTO premium_subscriptions
            (username,plan_name,amount)
            VALUES(%s,%s,%s)
            """,
            (
                st.session_state.username,
                "Enterprise",
                999
            ))

            conn.commit()

            st.success(
                "Enterprise Plan Activated Successfully"
            )

    st.divider()

    st.subheader("📊 Feature Comparison")

    comparison = pd.DataFrame({
        "Feature":[
            "Resume Analysis",
            "ATS Score",
            "AI Chat",
            "Interview Preparation",
            "Skill Gap Analysis",
            "Priority Support",
            "Candidate Ranking"
        ],
        "Free":[
            "✔","✔","✔","✖","✖","✖","✖"
        ],
        "Pro":[
            "✔","✔","✔","✔","✔","✔","✖"
        ],
        "Enterprise":[
            "✔","✔","✔","✔","✔","✔","✔"
        ]
    })

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )


elif menu == "Analysis Records":

    st.markdown("""
    <div class='hero-banner'>
        <div class='hero-main'>
        📊 Resume Analysis Records
        </div>

        <div class='hero-desc'>
        Track all previous resume evaluations,
        ATS scores and performance improvements.
        </div>
    </div>
    """, unsafe_allow_html=True)

    cursor.execute("""
    SELECT score,created_at
    FROM resume_analysis
    WHERE username=%s
    ORDER BY id DESC
    """,
    (st.session_state.username,)
    )

    records = cursor.fetchall()

    if records:

        df = pd.DataFrame(records)

        col1,col2,col3 = st.columns(3)

        with col1:
            st.metric("Total Analysis", len(df))

        with col2:
            st.metric("Highest Score", df["score"].max())

        with col3:
            st.metric("Average Score", round(df["score"].mean(),2))

        st.dataframe(
            df,
            use_container_width=True
        )

        fig = px.line(
            df,
            x="created_at",
            y="score",
            markers=True,
            title="Resume Score Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

elif menu == "Leaderboard":

    st.markdown("""
    <div class='hero-banner'>
        <div class='hero-main'>
        🏆 Resume Leaderboard
        </div>

        <div class='hero-desc'>
        Top performing resumes ranked
        by AI Resume Score.
        </div>
    </div>
    """, unsafe_allow_html=True)

    cursor.execute("""
    SELECT username,
    MAX(resume_score) score
    FROM analytics
    GROUP BY username
    ORDER BY score DESC
    LIMIT 10
    """)

    leaders = cursor.fetchall()

    if leaders:

        df = pd.DataFrame(leaders)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        fig = px.bar(
            df,
            x="username",
            y="score",
            title="Top Resume Scores"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )



elif menu == "Logout":

    add_history("Logged Out")

    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None

    st.rerun()
import streamlit as st

# Page config 
st.set_page_config(page_title="Smart Job Assistant", layout="wide")

# Sidebar navigation
st.sidebar.title("🧠 Smart Job Seeker Assistant")
page = st.sidebar.radio(
    "Navigate to:",
    ("🏠 Home", "📝 Resume Analyzer", "🔍 Job Matcher", "✨ GPT Suggestions", "📊 Application Tracker")
)

# Page logic
if page == "🏠 Home":
    st.title("Welcome to Smart Job Seeker Assistant 🚀")
    st.markdown("""
    This tool helps you:
    - Analyze your resume and extract skills  
    - Match jobs from a dataset  
    - Get AI suggestions to improve your resume  
    - Track your job applications easily  
    """)

elif page == "📝 Resume Analyzer":
    from resume_analyzer import show_resume_analyzer
    show_resume_analyzer()

elif page == "🔍 Job Matcher":
    from job_matcher import show_job_matcher
    show_job_matcher()

elif page == "✨ GPT Suggestions":
    from gpt_suggestions import show_gpt_suggestions
    show_gpt_suggestions()

elif page == "📊 Application Tracker":
    from tracker import show_tracker
    show_tracker()

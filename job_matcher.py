import streamlit as st
import pandas as pd

@st.cache_data
def load_jobs(file_path='jobs.csv'):
    return pd.read_csv(file_path)

def match_jobs(user_skills, job_df):
    def calculate_match(row):
        job_skills = set(map(str.strip, row['required_skills'].split(',')))
        matched = job_skills.intersection(user_skills)
        score = len(matched) / len(job_skills)
        return round(score * 100, 2), ", ".join(matched)

    job_df['match_score'], job_df['matched_skills'] = zip(*job_df.apply(calculate_match, axis=1))
    return job_df.sort_values(by='match_score', ascending=False)

def show_job_matcher():
    from resume_analyzer import show_resume_analyzer
    st.title("🔍 Job Matcher Based on Resume Skills")
    
    default_skills = ", ".join(st.session_state.get("extracted_skills", []))

    user_skills_input = st.text_input(
        "Paste extracted skills (comma-separated)",
        value=default_skills
    )
    #user_skills_input = st.text_input("Paste extracted skills (comma-separated)", "Python,SQL,Airflow") #static

    if user_skills_input:
        user_skills = set(map(str.strip, user_skills_input.split(',')))
        job_data = load_jobs()
        matched_jobs = match_jobs(user_skills, job_data)

        st.markdown("### 🧠 Top Matched Jobs")
        for _, row in matched_jobs.iterrows():
            st.markdown(f"""
            #### {row['role']} at {row['company']}
            📍 **Location**: {row['location']}  
            🎯 **Required Skills**: {row['required_skills']}  
            ✅ **Matched Skills**: {row['matched_skills']}  
            💯 **Match Score**: {row['match_score']}%
            ---
            """)

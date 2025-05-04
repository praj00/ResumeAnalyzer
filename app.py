import streamlit as st
import pdfplumber
import spacy
from db import SessionLocal
from models import Resume

st.title("Resume Analyzer - Upload your Resume")
uploaded_file=st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    st.subheader("Extracted Text:")
    st.write(text)


nlp = spacy.load("en_core_web_sm")

# Define a simple static skill list for now
skill_keywords = ["Python", "SQL", "Machine Learning", "Data Analysis", "AWS", "Azure", "ETL", "Data Engineering", "NLP"]
skills = []

def extract_skills(text):
    skills_found = []
    doc = nlp(text)
    for token in doc:
        if token.text in skill_keywords:
            skills_found.append(token.text)
    return list(set(skills_found))

if uploaded_file:
    skills = extract_skills(text)
    st.subheader("Skills Found:")
    st.write(skills)



# Input section
name = st.text_input("Name")
email = st.text_input("Email")
skills_text = ", ".join(skills) if skills else ""
skills_input = st.text_area("Skills (auto-filled)", value=skills_text)

# DB insert
def add_resume(name, email, skills):
    session = SessionLocal()
    new_resume = Resume(name=name, email=email, skills=skills)
    session.add(new_resume)
    session.commit()
    session.close()

if st.button("Save Resume"):
    add_resume(name, email, skills_input)
    st.success("Resume saved!")
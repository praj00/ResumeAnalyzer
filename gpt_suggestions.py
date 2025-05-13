import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

llm = ChatOpenAI(
    temperature=0.4,
    openai_api_key=st.secrets["openai"]["api_key"]  # ✅ Pass key directly
)

def show_gpt_suggestions():
    st.title("✨ GPT-Powered Resume Suggestions")

    # Input form
    with st.form("resume_edit_form"):
        resume_text = st.text_area("Paste your Resume text", height=250)
        job_description = st.text_area("Paste Job Description", height=250)
        submitted = st.form_submit_button("Suggest Resume Improvements")

    if submitted:
        if not resume_text or not job_description:
            st.warning("Please enter both resume and job description.")
            return

        with st.spinner("Thinking... 🤖"):
            response = get_gpt_suggestions(resume_text, job_description)
            st.success("Suggestions ready!")

            st.markdown("### 📌 Suggestions to Improve Your Resume:")
            st.markdown(response)

def get_gpt_suggestions(resume_text, job_desc):
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.4,
        openai_api_key=st.secrets["openai"]["api_key"]  # ✅ Fix added here too
    )

    prompt = ChatPromptTemplate.from_template("""
    You are a professional resume assistant.
    Given the resume below and a job description, suggest:
    - Better bullet points
    - Missing keywords/skills
    - Resume summary tailored to the role

    Resume:
    {resume}

    Job Description:
    {job_desc}

    Format response clearly using Markdown.
    """)

    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"resume": resume_text, "job_desc": job_desc})

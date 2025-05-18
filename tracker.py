# tracker.py

import streamlit as st
import models

def show_tracker():
    st.title("📊 Application Tracker (Multi-Link Enabled)")
    models.init_db()

    st.subheader("➕ Add a New Application")
    with st.form("add_form"):
        job_title = st.text_input("Job Title")
        company = st.text_input("Company")
        links_raw = st.text_area("Paste job links (comma-separated)")
        status = st.selectbox("Status", ["Applied", "Interview", "Offer", "Rejected"])
        submitted = st.form_submit_button("Add Application")

        if submitted:
            if job_title and company:
                links = [l.strip() for l in links_raw.split(",") if l.strip()]
                models.add_application(job_title, company, status, links)
                st.success("Application added successfully!")
            else:
                st.warning("Please enter both Job Title and Company.")

    st.subheader("📋 Your Applications")

    df = models.get_applications_with_links()
    if not df.empty:
        for _, row in df.iterrows():
            st.markdown(f"### {row['job_title']} at {row['company']}")
            
            if row['links']:
                for i, link in enumerate(row['links'], 1):
                    st.markdown(f"🔗 [Link {i}]({link})")
            else:
                st.text("No links added")

            st.markdown(f"🏷️ Status: **{row['status']}**")

            new_status = st.selectbox(
                f"Update status for {row['job_title']} at {row['company']}",
                ["Applied", "Interview", "Offer", "Rejected"],
                index=["Applied", "Interview", "Offer", "Rejected"].index(row['status']),
                key=f"status_{row['id']}"
            )

            if new_status != row['status']:
                models.update_status(row['id'], new_status)
                st.success(f"Updated status to {new_status}")
    else:
        st.info("No applications added yet.")

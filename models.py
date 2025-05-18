import sqlite3
import pandas as pd
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    skills = Column(String)

DB = "resume_analyzer.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        # Main table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_title TEXT,
                company TEXT,
                status TEXT
            );
        """)
        # Linked table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS application_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id INTEGER,
                link TEXT,
                FOREIGN KEY(application_id) REFERENCES applications(id) ON DELETE CASCADE
            );
        """)

def add_application(job_title, company, status, links):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO applications (job_title, company, status) VALUES (?, ?, ?)",
            (job_title, company, status)
        )
        app_id = cursor.lastrowid
        for link in links:
            cursor.execute(
                "INSERT INTO application_links (application_id, link) VALUES (?, ?)",
                (app_id, link.strip())
            )
        conn.commit()

def get_applications_with_links():
    with sqlite3.connect(DB) as conn:
        df_apps = pd.read_sql("SELECT * FROM applications", conn)
        df_links = pd.read_sql("SELECT * FROM application_links", conn)

        # Merge links into each application as list
        app_links = df_links.groupby("application_id")["link"].apply(list).to_dict()
        df_apps["links"] = df_apps["id"].map(app_links).fillna("").apply(lambda x: x if isinstance(x, list) else [])
        return df_apps

def update_status(app_id, new_status):
    with sqlite3.connect(DB) as conn:
        conn.execute(
            "UPDATE applications SET status = ? WHERE id = ?",
            (new_status, app_id)
        )
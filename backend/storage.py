import sqlite3
from datetime import datetime

DB_NAME = "assessment.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            language TEXT,
            skill TEXT,
            response TEXT,
            score INTEGER,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_response(student_name, language, skill, response, score=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        INSERT INTO responses (student_name, language, skill, response, score, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (student_name, language, skill, response, score, datetime.now().isoformat()))

    conn.commit()
    conn.close()


def get_all_responses():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT * FROM responses ORDER BY timestamp DESC")
    rows = c.fetchall()

    conn.close()
    return rows

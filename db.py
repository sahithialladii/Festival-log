# db.py
import sqlite3

def init_db():
    conn = sqlite3.connect("festival_log.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS festival_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            translated TEXT,
            keywords_telugu TEXT,
            image_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_entry(text, translated, keywords_telugu, image_path):
    conn = sqlite3.connect("festival_log.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO festival_entries (text, translated, keywords_telugu, image_path)
        VALUES (?, ?, ?, ?)
    ''', (text, translated, keywords_telugu, image_path))
    conn.commit()
    conn.close()

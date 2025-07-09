import sqlite3
import hashlib
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'scans.db')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS scans (
                hash TEXT PRIMARY KEY,
                filename TEXT,
                ela_image TEXT,
                score INTEGER,
                details TEXT,
                scanned_at TEXT
            )
        ''')
        conn.commit()

def hash_image(filepath):
    with open(filepath, 'rb') as f:
        file_data = f.read()
    return hashlib.sha256(file_data).hexdigest()

def get_scan_by_hash(image_hash):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM scans WHERE hash = ?', (image_hash,))
        row = c.fetchone()
        if row:
            return {
                'hash': row[0],
                'filename': row[1],
                'ela_image': row[2],
                'score': row[3],
                'details': row[4].split('||'),
                'scanned_at': row[5]
            }
    return None

def save_scan(image_hash, filename, ela_image, score, details):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO scans (hash, filename, ela_image, score, details, scanned_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            image_hash,
            filename,
            ela_image,
            score,
            '||'.join(details),
            datetime.now().isoformat()
        ))
        conn.commit()

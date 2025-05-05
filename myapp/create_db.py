import sqlite3
import os

# デプロイ先のパスにも対応できるように絶対パスで指定
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'data.db')

# DB接続とテーブル作成
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        content TEXT NOT NULL,
        image TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        likes INTEGER DEFAULT 0
    )
''')
conn.commit()
conn.close()

print("✅ postsテーブル作成完了")


import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()

c.execute('DROP TABLE IF EXISTS posts')
c.execute('''
    CREATE TABLE posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        content TEXT,
        image TEXT,
        timestamp TEXT
    )
''')

conn.commit()
conn.close()

print("新しいpostsテーブル作ったよ！")

import sqlite3

conn = sqlite3.connect("data.db")
c = conn.cursor()

try:
    c.execute("ALTER TABLE posts ADD COLUMN likes INTEGER DEFAULT 0")
except:
    print("既に追加されてるっぽい")

conn.commit()
conn.close()

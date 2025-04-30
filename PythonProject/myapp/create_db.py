import sqlite3

conn = sqlite3.connect("data.db")
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    content TEXT,
    image TEXT
)
''')

conn.commit()
conn.close()

conn = sqlite3.connect('data.db')
c = conn.cursor()
for row in c.execute('SELECT * FROM posts'):
    print(row)
conn.close()
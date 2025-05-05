import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename

# Flask アプリ設定
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "秘密のキー"

# DBパスを統一
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.db')

# --- 🔧 起動時にpostsテーブル作成 ---
def init_db():
    print("🔧 DB初期化中...")
    conn = sqlite3.connect(DB_PATH)
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

init_db()

# --- 仮ユーザー ---
users = {
    "test": "pass",
    "test2": "pass2"
}

# --- ログイン ---
@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("mypage"))
        else:
            message = "ユーザー名またはパスワードが違います"
    return render_template("login.html", message=message)

# --- マイページ ---
@app.route("/mypage")
def mypage():
    if "username" not in session:
        return redirect(url_for("login"))

    sort = request.args.get("sort", "new")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if sort == "likes":
        c.execute("SELECT id, user, content, image, timestamp, likes FROM posts ORDER BY likes DESC")
    else:
        c.execute("SELECT id, user, content, image, timestamp, likes FROM posts ORDER BY id DESC")

    posts = [{"id": row[0], "user": row[1], "content": row[2], "image": row[3], "timestamp": row[4], "likes": row[5]} for row in c.fetchall()]
    conn.close()

    return render_template("mypage.html", user=session["username"], posts=posts)

# --- 投稿 ---
@app.route("/post", methods=["POST"])
def post():
    if "username" not in session:
        return redirect(url_for("mypage"))

    content = request.form.get("content")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO posts (user, content, image, timestamp, likes) VALUES (?, ?, '', ?, 0)",
              (session["username"], content, timestamp))
    conn.commit()
    conn.close()

    return redirect(url_for("mypage"))

# --- 画像アップロード ---
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        if '画像' not in request.files:
            return '画像がアップロードされていません'

        file = request.files['画像']
        content = request.form.get('content', '')

        if file.filename == '':
            return 'ファイルが選択されていません'

        filename = secure_filename(file.filename)
        upload_path = os.path.join('static/uploads', filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file.save(upload_path)

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO posts (user, content, image, timestamp, likes) VALUES (?, ?, ?, ?, 0)",
                  (session['username'], content, filename, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()

        return redirect(url_for('mypage'))

    return render_template("upload.html")

# --- 投稿削除 ---
@app.route("/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    if "username" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("mypage"))

# --- いいね機能 ---
@app.route("/like/<int:post_id>", methods=["POST"])
def like_post(post_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE posts SET likes = likes + 1 WHERE id = ?", (post_id,))
    conn.commit()

    c.execute("SELECT likes FROM posts WHERE id = ?", (post_id,))
    new_likes = c.fetchone()[0]
    conn.close()

    return jsonify({"success": True, "likes": new_likes})

# --- 起動 ---
if __name__ == "__main__":
    app.run(debug=True)

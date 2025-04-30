import sqlite3
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session
import os

from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "秘密のキー"

# 仮のユーザー情報
users = {
    "test": "pass",
    "test2": "pass2"
}

# ログインページ
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

# マイページ
@app.route("/mypage")
def mypage():
    if "username" not in session:
        return redirect(url_for("login"))

    sort = request.args.get("sort", "new")  # デフォルトは新着順
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    if sort == "likes":
        c.execute("SELECT id, user, content, image, timestamp, likes FROM posts ORDER BY likes DESC")
    else:
        c.execute("SELECT id, user, content, image, timestamp, likes FROM posts ORDER BY id DESC")

    posts = [{"id": row[0], "user": row[1], "content": row[2], "image": row[3], "timestamp": row[4], "likes": row[5]} for row in c.fetchall()]
    conn.close()

    return render_template("mypage.html", user=session["username"], posts=posts)




@app.route("/post", methods=["POST"])
def post():
    if "username" not in session:
        return redirect(url_for("mypage"))

    content = request.form.get("content")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("INSERT INTO posts (user, content, image, timestamp, likes) VALUES (?, ?, '', ?, 0)",
              (session["username"], content, timestamp))
    conn.commit()
    conn.close()

    return redirect(url_for("mypage"))


# ログアウト
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if '画像' not in request.files:
            return '画像がアップロードされていません'

        file = request.files['画像']
        content = request.form.get('content', '')

        if file.filename == '':
            return 'ファイルが選択されていません'

        filename = secure_filename(file.filename)
        file.save(os.path.join('static/uploads', filename))

        # DBに保存
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("INSERT INTO posts (user, content, image, timestamp) VALUES (?, ?, ?, ?)",
                  (session['username'], content, filename, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()

        return redirect(url_for('mypage'))

    return render_template("upload.html")

# --- ① 削除用ルート追加 ---
@app.route("/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    if "username" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("mypage"))

from flask import jsonify

@app.route("/like/<int:post_id>", methods=["POST"])
def like_post(post_id):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("UPDATE posts SET likes = likes + 1 WHERE id = ?", (post_id,))
    conn.commit()

    c.execute("SELECT likes FROM posts WHERE id = ?", (post_id,))
    new_likes = c.fetchone()[0]
    conn.close()

    return jsonify({"success": True, "likes": new_likes})


if __name__ == "__main__":
    app.run(debug=True)

import sqlite3

conn = sqlite3.connect("data.db")
c = conn.cursor()

for row in c.execute('SELECT * FROM posts'):
    print(row)

conn.close()

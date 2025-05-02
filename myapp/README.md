# 📷 Flask投稿アプリ - ポートフォリオ作品

このアプリは、Flaskを使って開発したシンプルな**画像投稿＆共有SNS風アプリ**です。  
ログイン・投稿・画像アップロード・いいね機能・ソート（新着／人気順）など、基本的なSNS機能を備えています。

---

## 🚀 主な機能

- 🔐 ユーザーログイン（ユーザー名＋パスワード）
- 📝 メッセージ付きの投稿機能
- 📷 画像アップロード（JPEG, PNG）
- ❤️ いいね機能（リアルタイムカウント）
- 🔃 投稿ソート（新着順／いいね順）
- 🗑 投稿削除機能
- 🎨 シンプルなスタイルのUI（HTML＋CSS）

---

## 🛠 使用技術

| 項目 | 内容 |
|------|------|
| 言語 | Python 3.10 / HTML / CSS |
| フレームワーク | Flask |
| データベース | SQLite |
| その他 | Jinja2 / Werkzeug / GitHub管理 |

---

## 💡 使い方（ローカルで起動）

```bash
# 仮想環境を作成・有効化
python -m venv venv
venv\Scripts\activate      # Windows の場合

# ライブラリをインストール
pip install -r requirements.txt

# 初期DBを作成（任意のスクリプトがあればここに）
python create_db.py

# アプリを起動
python app.py
ブラウザで http://127.0.0.1:5000 を開くとアプリが表示されます。

👤 ログイン情報（デモ用）

ユーザー名	パスワード
test	pass
test2	pass2
📂 フォルダ構成（抜粋）
cpp
コピーする
編集する
├── myapp/
│   ├── static/
│   ├── templates/
│   ├── app.py
│   ├── create_db.py
│   └── data.db
├── requirements.txt
📝 今後の改善予定
アカウント登録機能の追加

コメント機能

投稿編集機能

デザインのアップグレード（BootstrapやTailwind導入）

📮 制作者
GitHub: @kisaki-kaede

ご覧いただきありがとうございます！

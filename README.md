<!--
# flask-edit-hameln-novel

## 概要
`flask-edit-hameln-novel` は、[Flask](https://flask.palletsprojects.com/en/3.0.x/)および[DrissionPage](https://github.com/g1879/DrissionPage)を使用してweb小説投稿サイト[ハーメルン](https://syosetu.org)へログインし、お気に入り登録された全ての小説のメモ及びタグを編集するツールです。


## 主な機能

1. ハーメルンへの自動ログイン
2. お気に入りに登録されている全小説の情報取得
3. 各小説のメモ欄に作品名と作者名を自動追記
4. 各小説のタグに作品名を自動追加

これにより、作品が削除された場合でも、どの作品が削除されたのかを容易に特定することができます。


## 必要環境

- Python 3.6以上
- DrissionPage
- Flask
- Flask-SocketIO
- Werkzeug


## 使用方法

1. このリポジトリをクローンし、必要なパッケージをインストールしてください。

```bash
git clone https://github.com/SahutoL/flask-edit-hameln-novel.git

cd flask-edit-hameln-novel
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

2. 以下のコマンドを実行してスクリプトを起動します：

```bash
python app.py
```

3. http://127.0.0.1:5000 へ移動してログイン情報の入力および編集情報の設定をして実行します。

## 動作の詳細

1. ハーメルンにログインします。
2. お気に入りページから全ての小説情報を取得します。
3. 各小説のページにアクセスし、以下の操作を行います：
   - メモ欄に「作品名：{作品名}」「作者名：{作者名}」を追記（既に同じ記述が存在する場合は追記しない）
   - タグに作品名を追加（既に存在する場合は追加しない）
4. 処理状況は画面下部に表示されます。
-->
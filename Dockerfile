# ベースイメージ
FROM python:3.9-slim

# 必要なパッケージをインストール
RUN apt-get update && \
    apt-get install -y \
    chromium-driver \
    chromium-browser && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 作業ディレクトリの設定
WORKDIR /app

# 依存関係をインストール
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# アプリケーションのコピー
COPY . .

# 環境変数の設定
ENV PATH="/usr/bin/chromium-browser:$PATH"

# ポートの公開
EXPOSE 5000

# アプリケーションの起動
CMD ["python", "app.py"]
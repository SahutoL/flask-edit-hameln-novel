# ベースイメージ
FROM python:3.9-slim

# 必要なパッケージをインストール
RUN apt-get update && \
    apt-get install -y \
    wget \
    gnupg \
    --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y \
    google-chrome-stable \
    --no-install-recommends && \
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
ENV PATH="/usr/bin/google-chrome:$PATH"

# ポートの公開
EXPOSE 5000

# アプリケーションの起動
CMD ["python", "app.py"]
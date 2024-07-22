FROM python:3.9

# Chrome依存関係のインストール
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get install -y \
    google-chrome-stable

# 作業ディレクトリの設定
WORKDIR /app

# 依存関係のインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードのコピー
COPY . .

# DrissionPage設定ファイルの作成
RUN mkdir -p /root/.config/DrissionPage && \
    echo '{"chrome_path":"/usr/bin/google-chrome-stable"}' > /root/.config/DrissionPage/config.json

ENV CHROMIUM_FLAGS="--disable-gpu --no-sandbox --disable-dev-shm-usage"

# 実行コマンド
CMD gunicorn --worker-class eventlet -w 1 app:app
# ベースイメージとしてPythonを使用
FROM python:3.9-slim

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y gcc

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# スクリプトをコンテナにコピー
COPY app.py .
COPY routes.py .
COPY services.py .
COPY openai.py .
COPY main.py .

# コンテナ起動時に実行するコマンドを設定
CMD ["python", "main.py"]
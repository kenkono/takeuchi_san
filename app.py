from flask import Flask
from routes import register_routes

# Flaskアプリケーションの作成
app = Flask(__name__)

# ルートの登録
register_routes(app)

if __name__ == '__main__':
    # アプリケーションの実行
    app.run(port=5000)
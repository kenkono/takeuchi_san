"""
クラス名：App
説明：Flaskアプリケーションのエントリーポイントを管理するクラス
"""

from flask import Flask
from routes import register_routes

class App:
    def __init__(self):
        # Flaskアプリケーションの作成
        self.app = Flask(__name__)
        # ルートの登録
        register_routes(self.app)

    def run(self, port=5000):
        # アプリケーションの実行
        self.app.run(port=port)
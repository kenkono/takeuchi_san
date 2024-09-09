"""
クラス名：Main
説明：メイン処理を行うクラス
"""

import threading
from pyngrok import ngrok
from services import TwilioService
from app import App

class Main:
    @staticmethod
    def start_flask_server():
        app_instance = App()
        app_instance.run(port=5000)

    @staticmethod
    def run():
        try:
            port = 5000
            # ngrokを使ってパブリックURLを取得
            public_url = ngrok.connect(port).public_url
            TwilioService.public_url = public_url

            # Flaskサーバーを別スレッドで起動
            flask_thread = threading.Thread(target=Main.start_flask_server)
            flask_thread.daemon = True
            flask_thread.start()

            # Twilioの通話を開始
            TwilioService.make_calls(public_url)

        except KeyboardInterrupt:
            print("KeyboardInterruptが検出されました。終了します...")

if __name__ == '__main__':
    Main.run()
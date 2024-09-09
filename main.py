import threading
from pyngrok import ngrok
from services import TwilioService

def start_flask_server():
    from app import app
    app.run(port=5000)

if __name__ == '__main__':
    try:
        port = 5000
        # ngrokを使ってパブリックURLを取得
        public_url = ngrok.connect(port).public_url
        TwilioService.public_url = public_url

        # Flaskサーバーを別スレッドで起動
        flask_thread = threading.Thread(target=start_flask_server)
        flask_thread.daemon = True
        flask_thread.start()

        # Twilioの通話を開始
        TwilioService.make_calls(public_url)

    except KeyboardInterrupt:
        print("KeyboardInterruptが検出されました。終了します...")
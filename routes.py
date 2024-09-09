from flask import request, jsonify, send_file
from twilio.twiml.voice_response import VoiceResponse
from services import TwilioService, AudioService, ConversationService

def register_routes(app):
    # TwiMLの生成ルート
    @app.route('/twiml', methods=['POST'])
    def twiml():
        response = VoiceResponse()
        response.play(TwilioService.get_public_url() + '/serve_audio')
        response.redirect('/start-recording')
        return str(response)

    # 音声ファイルの提供ルート
    @app.route('/serve_audio')
    def serve_audio():
        try:
            return send_file(AudioService.get_audio_file_path(), mimetype='audio/mpeg')
        except Exception as e:
            return jsonify(error=str(e)), 500

    # 録音開始のルート
    @app.route('/start-recording', methods=['POST'])
    def start_recording():
        response = VoiceResponse()
        response.record(max_length=60, action='/handle-recording', method="POST", transcribe=False)
        return str(response)

    # 録音処理のルート
    @app.route('/handle-recording', methods=['POST'])
    def handle_recording():
        recording_url = request.form['RecordingUrl']
        response = TwilioService.handle_recording(recording_url)
        return str(response)
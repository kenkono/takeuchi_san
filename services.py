import os
import time
import requests
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from pydub import AudioSegment
from openai import OpenAI
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class TwilioService:
    # Twilioの設定
    account_sid = os.getenv('TWILIO_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_number = os.getenv('TWILIO_PHONE_NUMBER')
    client = Client(account_sid, auth_token)
    public_url = None

    @staticmethod
    def get_public_url():
        return TwilioService.public_url

    @staticmethod
    def handle_recording(recording_url):
        # 録音ファイルの取得
        response = requests.get(recording_url, auth=(TwilioService.account_sid, TwilioService.auth_token))
        response.raise_for_status()
        audio_file_path = AudioService.save_audio_file(response.content)
        
        # 音声の文字起こし
        transcription = AudioService.transcribe_audio(audio_file_path)
        
        # 会話履歴の更新
        ConversationService.update_conversation_history(transcription)
        
        # 応答の生成
        response_text = ConversationService.generate_response()
        
        # テキストを音声に変換
        AudioService.text_to_speech(response_text)
        
        return TwilioService.create_twiml_response()

    @staticmethod
    def create_twiml_response():
        response = VoiceResponse()
        response.play(TwilioService.get_public_url() + '/serve_audio')
        response.redirect('/start-recording')
        return response

class AudioService:
    audio_file_path = 'audio.mp3'
    output_file_path = 'output.mp3'

    @staticmethod
    def save_audio_file(content):
        # 音声ファイルの保存
        with open(AudioService.audio_file_path, 'wb') as audio_file:
            audio_file.write(content)
        return AudioService.audio_file_path

    @staticmethod
    def transcribe_audio(audio_file_path):
        # 音声ファイルの文字起こし
        with open(audio_file_path, "rb") as audio_file:
            transcript = OpenAI.transcribe_audio(audio_file)
        return transcript

    @staticmethod
    def text_to_speech(text):
        # テキストを音声に変換して保存
        speech_file_path = Path(AudioService.output_file_path)
        response = OpenAI.text_to_speech(text)
        with open(speech_file_path, 'wb') as f:
            f.write(response.content)

    @staticmethod
    def get_audio_file_path():
        return AudioService.audio_file_path

class ConversationService:
    conversation_history = []

    @staticmethod
    def update_conversation_history(transcription):
        # 会話履歴の更新
        ConversationService.conversation_history.append({"role": "user", "content": transcription})

    @staticmethod
    def generate_response():
        # 応答の生成
        response = OpenAI.generate_response(ConversationService.conversation_history)
        ConversationService.conversation_history.append({"role": "system", "content": response})
        return response
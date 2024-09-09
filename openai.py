import openai

class OpenAI:
    @staticmethod
    def transcribe_audio(audio_file):
        # 音声ファイルの文字起こし
        return openai.Audio.transcriptions.create(model="whisper-1", file=audio_file, language="ja").text

    @staticmethod
    def generate_response(conversation_history):
        # 会話履歴に基づいて応答を生成
        response = openai.Chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたは不動産仲介会社の営業マンです。"},
                *conversation_history,
                {"role": "user", "content": "話し相手は電話口の不動産仲介会社です。"}
            ]
        )
        return response.choices[0].message.content

    @staticmethod
    def text_to_speech(text):
        # テキストを音声に変換
        return openai.Audio.speech.create(model="tts-1", voice="alloy", input=text)
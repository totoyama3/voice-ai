from groq import Groq
import secret_manager

METHOD = "whisper"

def transcribe_audio(wav_buffer):
    # Groq API クライアント
    key = secret_manager.api_manager("groq_api")

    try:
        client = Groq(api_key = key)
    except Exception as e:
        print(f"{METHOD}のクライアント取得でエラー発生しました")
        print(f"エラー内容：{e}")
        return None

    wav_buffer.seek(0)

    try:
        response = client.audio.transcriptions.create(
            file=("audio.wav", wav_buffer, "audio/wav"),
            model="whisper-large-v3",
            response_format="json"
        )
    except Exception as e:
        print(f"{METHOD}のAI処理中にエラー発生しました")
        print(f"エラー内容：{e}")
        return None

    # Whisperが返すテキスト
    text = response.text
    return text
    
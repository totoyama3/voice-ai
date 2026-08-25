from groq import Groq
import client_manager


def transcribe_audio(wav_buffer):
    """
    wav_buffer: STEP1で作った BytesIO の音声データ
    """
    # Groq API クライアント
    key = client_manager.api_manager("groq_api")
    client = Groq(api_key = key)


    wav_buffer.seek(0)

    response = client.audio.transcriptions.create(
        file=("audio.wav", wav_buffer, "audio/wav"),
        model="whisper-large-v3",
        response_format="json"
    )

    # Whisperが返すテキスト
    text = response.text
    return text
    
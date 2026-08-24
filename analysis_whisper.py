from groq import Groq

# Groq API クライアント
client = Groq(api_key="GROQ_API_KEY")

def transcribe_audio(wav_buffer):
    """
    wav_buffer: STEP1で作った BytesIO の音声データ
    """
    wav_buffer.seek(0)

    response = client.audio.transcriptions.create(
        file=("audio.wav", wav_buffer, "audio/wav"),
        model="whisper-large-v3",
        response_format="json"
    )

    # Whisperが返すテキスト
    text = response.text
    return text
    

if __name__ == "__main__":
    # STEP1の録音関数を使う
    from record import record_audio  # ← STEP1のコードを別ファイルにした場合

    wav_data = record_audio()
    text = transcribe_audio(wav_data)

    print("認識結果：", text)

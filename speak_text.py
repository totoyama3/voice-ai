import requests
import io
import wave
import simpleaudio as sa

VOICEVOX_URL = "http://127.0.0.1:50021"

# 話者ID
SPEAKER = 3


def speak(text):

    # 音声合成用のクエリを作成
    query_response = requests.post(
        f"{VOICEVOX_URL}/audio_query",
        params={
            "text": text,
            "speaker": SPEAKER
        }
    )

    query_response.raise_for_status()

    query = query_response.json()

    query["speedScale"] = 1.3

    # 音声合成
    synthesis_response = requests.post(
        f"{VOICEVOX_URL}/synthesis",
        params={
            "speaker": SPEAKER
        },
        json=query
    )

    synthesis_response.raise_for_status()

    # WAVデータを取得
    wav_data = synthesis_response.content

    # メモリ上のWAVを再生
    wav_file = wave.open(io.BytesIO(wav_data), "rb")

    audio = sa.WaveObject.from_wave_read(wav_file)

    play = audio.play()
    play.wait_done()

    wav_file.close()
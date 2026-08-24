import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import io

# ===== 設定 =====
SAMPLE_RATE = 16000  # Whisper推奨
DURATION = 3         # 録音秒数（まずは3秒）

def record_audio():
    print("録音開始（3秒）...")
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()
    print("録音終了")

    # numpy配列 → WAVバッファに変換
    wav_buffer = io.BytesIO()
    write(wav_buffer, SAMPLE_RATE, audio)
    wav_buffer.seek(0)

    return wav_buffer

if __name__ == "__main__":
    wav_data = record_audio()

    # 動作確認：ファイルとして保存（任意）
    with open("test.wav", "wb") as f:
        f.write(wav_data.read())

    print("test.wav を保存しました")

import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import io
import time

# ===== 設定 =====
SAMPLE_RATE = 16000  # Whisper推奨
DURATION = 0.5       # 録音秒数
SILENCE_TIME_LEVEL = 1.5   # 無音判定時間
SILENCE_VOLUME_LEVEL = 300  # 無音判定音声レベル

def record_audio():
    audio_data = []
    silent_time = None

    print(f"録音開始 {DURATION}s...")
    while True:
        audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
        sd.wait()
        volume_level = np.abs(audio).mean()
        audio_data.append(audio)
        if volume_level  > SILENCE_VOLUME_LEVEL:
            silent_time = time.time()
            print("録音中...")
        else:
            if silent_time is None:
                continue
            if (time.time() - silent_time) > SILENCE_TIME_LEVEL:
                print("録音中...")
                break
    print("録音終了")

    audio_data = np.concatenate(audio_data)

    # numpy配列 → WAVバッファに変換
    wav_buffer = io.BytesIO()
    write(wav_buffer, SAMPLE_RATE, audio_data)
    wav_buffer.seek(0)

    return wav_buffer
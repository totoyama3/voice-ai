import discord
from discord.ext import voice_recv
import secret_manager

from scipy.io.wavfile import write
from scipy.signal import resample_poly
import numpy as np
import io
import wave
import time
import threading

TOKEN = secret_manager.api_manager("discord_token")
VOICE_CHANNEL_NAME = secret_manager.name_manager("discord_server")

SAMPLE_RATE = 16000
SILENCE_TIME = 1.5
SILENCE_LEVEL = 500

intents = discord.Intents.default()
client = discord.Client(intents=intents)
callback = None
voice_client = None

class SpeechSink(voice_recv.AudioSink):

    def __init__(self):
        super().__init__()

        self.audio_data = []
        self.last_sound_time = None
        self.is_recording = False
        self.lock = threading.Lock()

        # 無音監視スレッド
        self.running = True
        self.monitor_thread = threading.Thread(
            target=self.monitor_silence,
            daemon=True
        )
        self.monitor_thread.start()

    def write(self, user, data):

        # Discordから受信したPCMデータ
        pcm_data = data.pcm

        if pcm_data is None:
            return

        # numpy配列へ変換
        audio = np.frombuffer(
            pcm_data,
            dtype=np.int16
        )

        # 音声のchを変換
        audio = audio.reshape(-1, 2)

        audio = audio.mean(axis=1)

        #audioのサンプルレートを16000に変換
        audio_16k = resample_poly(
            audio,
            16000,
            48000
        )

        audio_16k = audio_16k.astype(np.int16)

        # 音量計算
        volume_level = np.abs(audio).mean()

        with self.lock:

            # 音声がある
            if volume_level > SILENCE_LEVEL:

                if not self.is_recording:
                    print("発話開始")
                    self.is_recording = True

                self.audio_data.append(audio_16k)
                self.last_sound_time = time.time()

            # 無音
            elif self.is_recording:
                # 無音部分も音声データとして保存
                self.audio_data.append(audio_16k)

    def cleanup(self):
        print("音声受信終了")

    def process_audio(self):

        if not self.audio_data:
            return

        # 配列を結合
        audio = np.concatenate(
            self.audio_data
        )

        # WAVファイルとして保存
        write(
            "test_recprd.wav",
            16000,
            audio
        )

        # WAVへ変換
        wav_buffer = io.BytesIO()

        with wave.open(wav_buffer, "wb") as wav_file:

            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(SAMPLE_RATE)

            wav_file.writeframes(
                audio.tobytes()
            )
            wav_buffer.seek(0)

        if callback is not None:
            callback(wav_buffer)

        else:
            print("callbackが未設定です")


    def wants_opus(self):
        return False

    def monitor_silence(self):
        while self.running:
            time.sleep(0.1)
            with self.lock:
                if not self.is_recording:
                    continue
                if self.last_sound_time is None:
                    continue
                silent_time = time.time() - self.last_sound_time
                if silent_time >= SILENCE_TIME:
                    print("発話終了")
                    self.process_audio()
                    self.audio_data = []
                    self.last_sound_time = None
                    self.is_recording = False


#音声を再生する
def play_audio(file_path):

    if voice_client is None:
        print("ボイスチャンネルに接続していません")
        return

    if voice_client.is_playing():
        print("現在、音声を再生中です")
        return

    audio_source = discord.FFmpegPCMAudio(
        file_path
    )

    voice_client.play(
        audio_source
    )

    print("Discordで音声再生開始")


@client.event
async def on_ready():
    global voice_client

    print(f"ログインしました: {client.user}")

    for guild in client.guilds:

        for channel in guild.voice_channels:

            if channel.name == VOICE_CHANNEL_NAME:

                if guild.voice_client is not None:
                    print("すでに接続しています")
                    return

                print(
                    f"接続開始: {channel.name}"
                )

                voice_client = await channel.connect(
                    cls=voice_recv.VoiceRecvClient
                )

                print("ボイスチャンネルに接続しました")

                # 音声受信開始
                sink = SpeechSink()

                voice_client.listen(sink)

                print("音声受信開始")

                return

    print("ボイスチャンネルが見つかりません")



def client_run(method):
    global callback
    callback = method
    client.run(TOKEN)
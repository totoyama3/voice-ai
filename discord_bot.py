import discord
from discord.ext import voice_recv
import secret_manager

TOKEN = secret_manager.api_manager("discord_token")

VOICE_CHANNEL_NAME = secret_manager.name_manager("discord_server")

intents = discord.Intents.default()

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"ログインしました: {client.user}")

    for guild in client.guilds:
        for channel in guild.voice_channels:

            if channel.name == VOICE_CHANNEL_NAME:

                if guild.voice_client is not None:
                    print("すでに接続しています")
                    return

                print(f"接続開始: {channel.name}")

                voice_client = await channel.connect(
                    cls=voice_recv.VoiceRecvClient
                )

                print("ボイスチャンネルに接続しました")

                # 音声受信開始
                voice_client.listen(
                    voice_recv.WaveSink("discord_audio.wav")
                )

                print("音声受信開始")
                return

    print("指定したボイスチャンネルが見つかりません")


client.run(TOKEN)
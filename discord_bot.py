import discord
import secret_manager

TOKEN = secret_manager.api_manager("discord_token")
VOICE_CHANNEL_NAME = secret_manager.name_manager("discord_server")
# Botに必要な権限
intents = discord.Intents.default()

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"ログインしました: {client.user}")

    for guild in client.guilds:
        for channel in guild.voice_channels:
            if channel.name == VOICE_CHANNEL_NAME:
                if guild.voice_client is not None:
                    print("すでにボイスチャンネルへ接続しています")
                    return
                print(f"接続開始: {channel.name}")

                await channel.connect()

                print("接続完了")
                return

    print("指定したボイスチャンネルが見つかりません")


client.run(TOKEN)
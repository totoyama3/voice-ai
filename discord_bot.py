import discord
import client_manager

TOKEN = client_manager.api_manager("discord")

# Botに必要な権限
intents = discord.Intents.default()

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"ログインしました: {client.user}")


client.run(TOKEN)
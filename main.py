import discord
from client import Client
from dotenv import load_dotenv
import os

load_dotenv()
token: str | None = os.getenv("SUNFLOWER_TOKEN")
if token is None:
    raise ValueError("No token found in environment variables.")
print(f"Loaded Token: {token[:10]}...")

intents = discord.Intents.default()
intents.message_content = True
activity = discord.Activity(type=discord.ActivityType.playing, name="Archiving your messages")

client = Client(intents=intents, activity=activity)
client.run(token)

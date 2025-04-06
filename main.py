import discord
from dotenv import load_dotenv
import os

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.lower().startswith('!hello'):
            await message.channel.send(f"Hello {message.author.name}!")
            print( f"Message content: {message.content}")

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
token = os.getenv("SUNFLOWER_TOKEN")
print(f"Token: {token}")

client = Client(intents=intents)
client.run(token)

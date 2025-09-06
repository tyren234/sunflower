import discord
from utils.messages import *

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        channel = message.channel
        if not isinstance(channel, discord.TextChannel):
            await message.channel.send("This bot can only be used in a server text channel.")
            return
        channel_name: str = channel.name

        if message.content.lower().startswith('!hello'):
            await message.channel.send(f"This message was sent on {message.channel.id}: {channel_name}")
            print(f"Message content: {message.content}")

        if message.content.lower().startswith('!channels'):
            await message.channel.send(f"All channels I can see are: {list(self.get_all_channels())}.")
        
        if message.content.lower().startswith('!firstmsg'):
            counter = await count_messages(channel)
            await message.channel.send(f"This channel has {counter} messages in it.")
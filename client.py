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

        if message.content.lower() == '!help':
            await message.channel.send(get_help_message())

        if message.content.lower() == '!channel':
            await message.channel.send(f"This message was sent on {message.channel.id}: {channel_name}")
            print(f"Message content: {message.content}")

        if message.content.lower() == '!count':
            counter = await count_messages_in_channel(channel)
            await message.channel.send(f"This channel has {counter} messages in it.")
import discord
from utils.messages import *
from utils.commons import is_message_invalid

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        if is_message_invalid(message):
            await message.channel.send("This bot can only be used in a server text channel.")
            return

        if message.content.lower() == '!help':
            await message.channel.send(get_help_message())

        if message.content.lower() == '!info':
            await message.channel.send(get_message_info(message))

        assert isinstance(message.channel, discord.TextChannel)
        channel: discord.TextChannel = message.channel
        if message.content.lower() == '!count':
            counter = await count_messages_in_channel(channel)
            await message.channel.send(f"This channel has {counter} messages in it.")
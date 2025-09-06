import discord
from commands.count import perform_count_messages_in_channel
from commands.help import perform_help_message
from commands.save import perform_save_message
from commands.backup import perform_channel_backup
from commands.info import perform_message_info
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

        if message.content.lower().startswith('!help'):
            await perform_help_message(message)
        elif message.content.lower().startswith('!info'):
            await perform_message_info(message)
        elif message.content.lower().startswith("!save"):
            await perform_save_message(message)
        elif message.content.lower().startswith("!backup"):
            await perform_channel_backup(message)
        elif message.content.lower().startswith('!count'):
            assert isinstance(message.channel, discord.TextChannel)
            channel: discord.TextChannel = message.channel
            await perform_count_messages_in_channel(channel)
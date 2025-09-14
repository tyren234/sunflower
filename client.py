import discord
from commands.count import perform_count_messages_in_channel
from commands.help import perform_help_message
from commands.last import perform_last
from commands.save import perform_save_message
from commands.backup import perform_channel_backup
from commands.info import perform_message_info
from commands.backup_new_messages import perform_backup_new_messages

from utils.commons import is_message_invalid, sunflower_send
import load_env
from utils.saving import backup_new_messages

class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")
        load_env.load_output_channel_id()
        # `sunflower_output_channel` and `sunflower_output_channel_id` are global! Watch out!
        if load_env.sunflower_output_channel_id is not None:
            channel = await self.fetch_channel(int(load_env.sunflower_output_channel_id))
            if isinstance(channel, discord.abc.Messageable):
                load_env.sunflower_output_channel = channel
        print("Will send updates to a channel" if load_env.sunflower_output_channel is not None else "Won't send updates to a channel. Channel not found.")

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        if is_message_invalid(message):
            await message.channel.send("This bot can only be used in a server text channel.")
            return

        if message.content.lower().startswith("!help"):
            await perform_help_message(message)
        elif message.content.lower().split(" ")[0] == "!info":
            await perform_message_info(message)
        elif message.content.lower().split(" ")[0] == "!save":
            await perform_save_message(message)
        elif message.content.lower().split(" ")[0] == "!backup":
            await perform_channel_backup(message)
        elif message.content.lower().split(" ")[0] == "!backupnew":
            await perform_backup_new_messages(message)
        elif message.content.lower().startswith("!last"):
            await perform_last(message)
        elif message.content.lower().startswith("!count"):
            assert isinstance(message.channel, discord.TextChannel)
            channel: discord.TextChannel = message.channel
            await perform_count_messages_in_channel(channel)
        # Just backup the message
        else:
            if not isinstance(message.channel, discord.TextChannel):
                print(f"Can't backup non-text channels.")
                await sunflower_send(f"Can't backup non-text channels.", message)
                return
            no_backed_up_messages: int = await backup_new_messages(message.channel)
            if no_backed_up_messages > 0:
                await sunflower_send(f"Successfully backed up {no_backed_up_messages} messages from {message.channel.jump_url}.", message)
            else:
                await sunflower_send(f"Failed to save messages from {message.channel.jump_url}.", message)


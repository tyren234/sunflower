import discord
from pathlib import Path
from utils.files import get_save_path
# from utils.urls import get_message_url_from_message
from utils.commons import is_message_invalid

async def perform_count_messages_in_channel(channel: discord.TextChannel) -> None:
    counter = 0
    async for _ in channel.history(limit=None):
        counter += 1
    await channel.send(f"This channel has {counter} messages in it.")

async def perform_help_message(message: discord.Message) -> None:
    help_text = (
        "\nAvailable commands:\n"
        "`!help` - Show this help message\n"
        "`!info` - Show info about this message\n"
        "`!count` - Count messages in the current channel\n"
        "`!save <message id>` - Save a specific message from this channel to a file\n"
        "`!save <message id> <channel id>` - Save a specific message from a specified channel to a file\n"
        "`!backup` - Backup all messages in the current channel to a file (doesn't work yet)\n"
    )
    await message.channel.send(help_text)

async def perform_message_info(message: discord.Message) -> None:
    info_text = (
        f"Message ID: {message.id}\n"
        f"URL to this message: {message.jump_url}\n"
        f"Author: {message.author} (ID: {message.author.id})\n"
        f"Channel: {message.channel} (ID: {message.channel.id})\n"
        f"Guild: {message.guild} (ID: {message.guild.id if message.guild is not None else "Hasn't got ID"})\n"
        f"Created at: {message.created_at}\n"
        f"Edited at: {message.edited_at}\n"
        f"Attachments: {[attachment.url for attachment in message.attachments]}\n" 
        )
    await message.channel.send(info_text)


async def backup_channel(channel: discord.TextChannel, backup_path: Path ) -> None:
    pass

'''
Arguments:
    message: discord.Message - message containing the command. It should specify what message to save.
        Format should look like this: "!save <message id>" where <message id> is the ID of a message in the same channel
        or "!save <message id> <channel id>" where <channel id> is the ID of the channel containing the message.
'''
async def perform_save_message(message: discord.Message) -> None:
    assert message.content is not None
    content = message.content.strip().split(" ")
    if len(content) not in [2, 3]:
        await message.channel.send("Invalid command format. Use `!save <message id>` or `!save <message id> <channel id>`.")
        return
    assert message.channel is not None and message.guild is not None
    assert isinstance(message.channel, discord.TextChannel)
    if len(content) == 2:
        message_id: int = int(content[1])
        channel = message.channel
    else:
        message_id: int = int(content[1])
        channel_id: int = int(content[2])
        channel = message.guild.get_channel(channel_id)
        if channel is None or not isinstance(channel, discord.TextChannel):
            await message.channel.send(f"Channel with ID `{channel_id}` not found or is not a text channel.")
            return
    assert isinstance(channel, discord.TextChannel)
    try:
        message_to_save: discord.Message = await channel.fetch_message(message_id)
    except:
        await message.channel.send(f"Message with ID `{message_id}` not found in channel {channel.jump_url}.")
        return

    if await save_message(message_to_save):
        await message.channel.send(f"Message {message_to_save.jump_url} saved successfully.")
    else:
        await message.channel.send(f"Failed to save message {message_to_save.jump_url}.")

async def save_message(message: discord.Message) -> bool:
    assert isinstance(message.channel, discord.TextChannel) and message.guild is not None
    return await save_message_to_file(message, get_save_path(message.guild.name, message.channel.name))

async def save_message_to_file(message: discord.Message, file_path: Path) -> bool:
    if is_message_invalid(message):
        print(f"Message {message.id} is invalid, not saving.")
        return False
    
    assert message.guild is not None

    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("a", encoding="utf-8") as file:
        file.write(f"\n\n{message.created_at:%Y-%m-%d %H:%M:%S} [{message.id}]({message.jump_url})\n\n{message.content}\n")
    return True

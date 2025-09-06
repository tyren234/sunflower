import discord
from pathlib import Path
from utils.files import get_save_path

async def count_messages_in_channel(channel: discord.TextChannel) -> int:
    counter = 0
    async for _ in channel.history(limit=None):
        counter += 1
    return counter

def get_help_message() -> str:
    help_text = (
        "\nAvailable commands:\n"
        "`!help` - Show this help message\n"
        "`!info` - Show info about this message\n"
        "`!count` - Count messages in the current channel\n"
        "`!backup` - Backup all messages in the current channel to a file\n"
    )
    return help_text

def get_message_info(message: discord.Message) -> str:
    info_text = (
        f"Message ID: {message.id}\n"
        f"Author: {message.author} (ID: {message.author.id})\n"
        f"Channel: {message.channel} (ID: {message.channel.id})\n"
        f"Guild: {message.guild} (ID: {message.guild.id if message.guild is not None else "Hasn't got ID"})\n"
        f"Created at: {message.created_at}\n"
        f"Edited at: {message.edited_at}\n"
        f"Attachments: {[attachment.url for attachment in message.attachments]}\n" 
        )
    return info_text

async def backup_channel(channel: discord.TextChannel, backup_path: Path ) -> None:
    pass

async def save_message(message: discord.Message, guild_name: str, channel_name: str) -> None:
    await save_message_to_file(message, get_save_path(guild_name, channel_name))

async def save_message_to_file(message: discord.Message, file_path: Path) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("a", encoding="utf-8") as file:
        file.write(f"\nid:[{message.id}]\n{message.content}\n")

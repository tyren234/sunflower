import discord
from pathlib import Path

async def count_messages_in_channel(channel: discord.TextChannel) -> int:
    counter = 0
    async for _ in channel.history(limit=None):
        counter += 1
    return counter

def get_help_message() -> str:
    help_text = (
        "Available commands:\n"
        "!help - Show this help message\n"
        "!channel - Show the current channel name and id\n"
        "!count - Count messages in the current channel\n"
        "!backup - Backup all messages in the current channel to a file\n"
    )
    return help_text

async def backup_channel(channel: discord.TextChannel, backup_path: Path ) -> None:
    pass

async def save_message_to_file(message: discord.Message, file_path: Path) -> None:
    pass

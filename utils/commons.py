import discord
from pathlib import Path

def is_message_invalid(message: discord.Message) -> bool:
    if message.guild is None or not isinstance(message.channel, discord.TextChannel):
        print(f"Message {message.id} in channel {message.channel.id} is invalid.")
        return True
    return False

def get_attachments_paths_as_markdown_links(paths: list[Path]) -> list[str]:
    output: list[str] = []
    for path in paths:
        output.append(f"[{path.name}]({path})")

    return output

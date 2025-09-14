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
    
def get_message_header_string(message: discord.Message) -> str:
    return f"{message.created_at:%Y-%m-%d %H:%M:%S} [{message.id}]({message.jump_url})"

def get_message_footer_string() -> str:
    return "---"

def add_header_and_footer_to_message_string(message: discord.Message, message_string: str) -> str:
    return f"{get_message_header_string(message)}\n\n{message_string}\n\n{get_message_footer_string()}\n\n"

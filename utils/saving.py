import discord
from pathlib import Path
from utils.files import get_save_path
from utils.commons import is_message_invalid 

async def save_message(message: discord.Message, override_file: bool = False) -> bool:
    assert isinstance(message.channel, discord.TextChannel) and message.guild is not None
    return await save_message_to_file(message, get_save_path(message.guild.name, message.channel.name), override_file)

async def save_message_to_file(message: discord.Message, file_path: Path, override_file: bool) -> bool:
    if is_message_invalid(message):
        print(f"Message {message.id} is invalid, not saving.")
        return False
    save_string_to_file(get_message_string(message), file_path, override_file)
    return True    

def save_string_to_file(string: str, file_path: Path, override_file: bool) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("a" if not override_file else "w", encoding="utf-8") as file:
        file.write(string)

def create_message_string_from_messages(messages: list[discord.Message]) -> str:
    message_strings = [get_message_string(msg) for msg in messages]
    return "".join(message_strings)

def get_message_string(message: discord.Message) -> str:
    return f"{message.created_at:%Y-%m-%d %H:%M:%S} [{message.id}]({message.jump_url})\n\n{message.content}\n\n"

async def backup_channel(channel: discord.TextChannel) -> int:
    messages: list[discord.Message] = []
    async for message in channel.history(limit=None, oldest_first=True):
        if is_message_invalid(message):
            print(f"Message {message.id} is invalid, not saving.")
            continue
        messages.append(message)

    save_string_to_file(create_message_string_from_messages(messages), get_save_path(channel.guild.name, channel.name), override_file=True)
    return len(messages)
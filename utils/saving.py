import discord
from pathlib import Path
from utils.files import download_attachments, get_save_path
from utils.commons import get_attachments_paths_as_markdown_links, is_message_invalid 

async def save_message(message: discord.Message, override_file: bool = False) -> bool:
    assert isinstance(message.channel, discord.TextChannel) and message.guild is not None
    return await save_message_to_file(message, get_save_path(message.guild.name, message.channel.name), override_file)

async def save_message_to_file(message: discord.Message, file_path: Path, override_file: bool) -> bool:
    if is_message_invalid(message):
        print(f"Message {message.id} is invalid, not saving.")
        return False
    
    attachments_paths = await download_attachments(message.attachments, name_prefix=str(message.id))
    message_string = get_message_string(message, attachments_paths)

    save_string_to_file(message_string, file_path, override_file)

    return True    

def save_string_to_file(string: str, file_path: Path, override_file: bool) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("a" if not override_file else "w", encoding="utf-8") as file:
        file.write(string)

async def create_message_string_from_messages(messages: list[discord.Message]) -> str:
    message_strings: list[str] = []
    for message in messages:
        attachments_paths = await download_attachments(message.attachments, name_prefix=str(message.id))
        message_strings.append(get_message_string(message, attachments_paths))

    return "".join(message_strings)

def get_message_string(message: discord.Message, attachments_paths: list[Path] = []) -> str:
    message_string = f"{message.created_at:%Y-%m-%d %H:%M:%S} [{message.id}]({message.jump_url})\n\n{message.content}\n\n"
    if len(attachments_paths) > 0:
        markdown_links = get_attachments_paths_as_markdown_links(attachments_paths)
        message_string += " ".join(markdown_links) + "\n\n"
    message_string += "---\n\n"
    print(f"Got message {message.id} string.")
    return message_string

async def backup_channel(channel: discord.TextChannel) -> int:
    messages: list[discord.Message] = []
    async for message in channel.history(limit=None, oldest_first=True):
        if is_message_invalid(message):
            print(f"Message {message.id} is invalid, not saving.")
            continue
        messages.append(message)

    save_string_to_file(await create_message_string_from_messages(messages), get_save_path(channel.guild.name, channel.name), override_file=True)
    return len(messages)
import discord
from pathlib import Path
from utils.files import download_attachments, get_save_path, get_last_message_url_and_id_from_file
from utils.commons import get_attachments_paths_as_markdown_links, is_message_invalid, add_header_and_footer_to_message_string

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
    message_string = message.content
    if len(attachments_paths) > 0:
        markdown_links = get_attachments_paths_as_markdown_links(attachments_paths)
        message_string += " ".join(markdown_links) + "\n\n"
    
    message_string = add_header_and_footer_to_message_string(message, message_string)
    print(f"Got message {message.id} string.")
    return message_string

async def backup_channel_after_message(channel: discord.TextChannel, after_message: discord.Message | None) -> int:
    """
    Backup all messages in the channel after given message.
    If message is `None`, backup all messages in the channel.

    Args:
        channel (discord.TextChannel): Channel to backup.
        message (discord.Message | None): Message after which to backup. If `None`, backup all messages in the `channel`.

    Returns:
        int: Number of backed up messages.
    """
    messages: list[discord.Message] = []
    async for message in channel.history(limit=None, oldest_first=True, after=after_message):
        if is_message_invalid(message):
            print(f"Message {message.id} is invalid, not saving.")
            continue
        messages.append(message)

    save_string_to_file(await create_message_string_from_messages(messages), get_save_path(channel.guild.name, channel.name), override_file=True if after_message is None else False)
    return len(messages)

# TODO: Change the name later to something like backup_channel_new_messages
async def backup_new_messages(channel: discord.TextChannel) -> int:
    save_path = get_save_path(channel.guild.name, channel.name)
    last_saved_id = get_last_message_url_and_id_from_file(save_path)
    
    if last_saved_id is None:
        # If no messages were saved before, do a full backup
        return await backup_channel_after_message(channel, None)
        
    try:
        last_message = await channel.fetch_message(last_saved_id[1])
    except discord.NotFound:
        print(f"Last saved message {last_saved_id} not found in channel {channel.name}")
        return 0
        
    return await backup_channel_after_message(channel, last_message)
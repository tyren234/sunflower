import discord
from pathlib import Path
from utils.files import get_save_path
from utils.commons import is_message_invalid 

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

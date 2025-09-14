import discord
from utils.files import get_last_message_url_and_id_from_file, get_save_path

async def perform_last(request_message: discord.Message) -> None:
    assert isinstance(request_message.channel, discord.TextChannel) and request_message.guild is not None
    (last_message_url, last_message_id) = get_last_message_url_and_id_from_file(get_save_path(request_message.guild.name, request_message.channel.name)) or ("Not found", "URL not found")
    await request_message.channel.send(f"Last saved message from this file has ID: `{last_message_id}`: {last_message_url}")
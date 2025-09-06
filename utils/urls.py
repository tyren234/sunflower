import discord
from utils.commons import is_message_invalid
DISCORD_MESSAGE_URL_PREFIX = "https://discord.com/channels"

def get_message_url(guild_id: int, channel_id: int, message_id: int) -> str:
    return f"{DISCORD_MESSAGE_URL_PREFIX}/{guild_id}/{channel_id}/{message_id}"

def get_message_url_from_message(message: discord.Message) -> str:
    if is_message_invalid(message):
        return "Invalid message"
    assert message.guild is not None
    return get_message_url(message.guild.id, message.channel.id, message.id)
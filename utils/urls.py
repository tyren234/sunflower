DISCORD_MESSAGE_URL_PREFIX = "https://discord.com/channels"

def get_message_url(guild_id: int, channel_id: int, message_id: int) -> str:
    return f"{DISCORD_MESSAGE_URL_PREFIX}/{guild_id}/{channel_id}/{message_id}"
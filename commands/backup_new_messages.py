import discord
from utils.saving import backup_new_messages

async def perform_backup_new_messages(request_message: discord.Message) -> None:
    """Backup new messages in the channel since the last saved message.

    Args:
        channel (discord.TextChannel): The channel to backup messages from.

    Returns:
        None
    """
    assert request_message.content is not None and request_message.channel is not None and request_message.guild is not None
    content = request_message.content.strip().split(" ")
    if len(content) != 2:
        await request_message.channel.send("Invalid command format. Use `!backupnew <channel id>`.")
        return 

    channel_id: int = int(content[1])
    try:
        channel_to_backup = await request_message.guild.fetch_channel(channel_id)
    except:
        await request_message.channel.send(f"Channel with ID `{channel_id}` not found.")
        return
    if not isinstance(channel_to_backup, discord.TextChannel):
        await request_message.channel.send(f"Channel {channel_to_backup.jump_url} is not a text channel.")
        return
    
    await backup_new_messages(channel_to_backup)
    return
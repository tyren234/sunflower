import discord
from utils.saving import backup_channel

async def perform_channel_backup(request_message: discord.Message) -> None:
    assert request_message.content is not None
    content = request_message.content.strip().split(" ")
    if len(content) is not 2:
        await request_message.channel.send("Invalid command format. Use `!backup <channel id>` or `!backup`.")
        return
    assert request_message.channel is not None and request_message.guild is not None

    channel_id: int = int(content[1])
    try:
        channel_to_backup = await request_message.guild.fetch_channel(channel_id)
    except:
        await request_message.channel.send(f"Channel with ID `{channel_id}` not found.")
        return

    if not isinstance(channel_to_backup, discord.TextChannel):
        await request_message.channel.send(f"Channel {channel_to_backup.jump_url} is not a text channel.")
        return
    
    no_backed_up_messages: int = await backup_channel(channel_to_backup)
    if no_backed_up_messages > 0:
        await request_message.channel.send(f"Successfully backed up {no_backed_up_messages} messages from {channel_to_backup.jump_url}.")
    else:
        await request_message.channel.send(f"Failed to save messages from {channel_to_backup.jump_url}.")
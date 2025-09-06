import aiohttp
import discord

from utils.files import get_asset_path

async def perform_message_info(request_message: discord.Message) -> None:
    assert request_message.content is not None
    content = request_message.content.strip().split(" ")
    if len(content) not in [2, 3]:
        await request_message.channel.send("Invalid command format. Use `!info <message id>` or `!info <message id> <channel id>`.")
        return
    assert request_message.channel is not None and request_message.guild is not None
    assert isinstance(request_message.channel, discord.TextChannel)
    if len(content) == 2:
        message_id: int = int(content[1])
        channel = request_message.channel
    else:
        message_id: int = int(content[1])
        channel_id: int = int(content[2])
        channel = request_message.guild.get_channel(channel_id)
        if channel is None or not isinstance(channel, discord.TextChannel):
            await request_message.channel.send(f"Channel with ID `{channel_id}` not found or is not a text channel.")
            return
    assert isinstance(channel, discord.TextChannel)
    try:
        message_to_info: discord.Message = await channel.fetch_message(message_id)
    except:
        await request_message.channel.send(f"Message with ID `{message_id}` not found in channel {channel.jump_url}.")
        return

    for attachment in message_to_info.attachments:
        async with aiohttp.ClientSession() as session:
            async with session.get(attachment.url) as r:
                if r.status == 200:
                    with open(get_asset_path(attachment.filename), "wb") as handler:
                        handler.write(await r.read())

    info_text = (
        f"Message ID: {message_to_info.id}\n"
        f"URL to this message: {message_to_info.jump_url}\n"
        f"Author: {message_to_info.author} (ID: {message_to_info.author.id})\n"
        f"Channel: {message_to_info.channel} (ID: {message_to_info.channel.id})\n"
        f"Guild: {message_to_info.guild} (ID: {message_to_info.guild.id if message_to_info.guild is not None else "Hasn't got ID"})\n"
        f"Created at: {message_to_info.created_at}\n"
        f"Edited at: {message_to_info.edited_at}\n"
        f"Attachments: {[attachment.url for attachment in message_to_info.attachments]}\n" 
        )
    
    await request_message.channel.send(info_text)
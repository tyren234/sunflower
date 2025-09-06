import discord
from utils.messages import save_message

'''
Arguments:
    message: discord.Message - message containing the command. It should specify what message to save.
        Format should look like this: "!save <message id>" where <message id> is the ID of a message in the same channel
        or "!save <message id> <channel id>" where <channel id> is the ID of the channel containing the message.
'''
async def perform_save_message(message: discord.Message) -> None:
    assert message.content is not None
    content = message.content.strip().split(" ")
    if len(content) not in [2, 3]:
        await message.channel.send("Invalid command format. Use `!save <message id>` or `!save <message id> <channel id>`.")
        return
    assert message.channel is not None and message.guild is not None
    assert isinstance(message.channel, discord.TextChannel)
    if len(content) == 2:
        message_id: int = int(content[1])
        channel = message.channel
    else:
        message_id: int = int(content[1])
        channel_id: int = int(content[2])
        channel = message.guild.get_channel(channel_id)
        if channel is None or not isinstance(channel, discord.TextChannel):
            await message.channel.send(f"Channel with ID `{channel_id}` not found or is not a text channel.")
            return
    assert isinstance(channel, discord.TextChannel)
    try:
        message_to_save: discord.Message = await channel.fetch_message(message_id)
    except:
        await message.channel.send(f"Message with ID `{message_id}` not found in channel {channel.jump_url}.")
        return

    if await save_message(message_to_save):
        await message.channel.send(f"Message {message_to_save.jump_url} saved successfully.")
    else:
        await message.channel.send(f"Failed to save message {message_to_save.jump_url}.")
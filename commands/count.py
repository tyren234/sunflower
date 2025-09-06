import discord

async def perform_count_messages_in_channel(channel: discord.TextChannel) -> None:
    counter = 0
    async for _ in channel.history(limit=None):
        counter += 1
    await channel.send(f"This channel has {counter} messages in it.")
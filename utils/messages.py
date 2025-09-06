import discord

async def count_messages(channel: discord.TextChannel) -> int:
    counter = 0
    async for _ in channel.history(limit=None):
        counter += 1
    return counter

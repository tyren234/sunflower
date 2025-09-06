import discord

def is_message_invalid(message: discord.Message) -> bool:
    if message.guild is None or not isinstance(message.channel, discord.TextChannel):
        print(f"Message {message.id} in channel {message.channel.id} is invalid.")
        return True
    return False
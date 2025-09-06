import discord

async def perform_message_info(message: discord.Message) -> None:
    info_text = (
        f"Message ID: {message.id}\n"
        f"URL to this message: {message.jump_url}\n"
        f"Author: {message.author} (ID: {message.author.id})\n"
        f"Channel: {message.channel} (ID: {message.channel.id})\n"
        f"Guild: {message.guild} (ID: {message.guild.id if message.guild is not None else "Hasn't got ID"})\n"
        f"Created at: {message.created_at}\n"
        f"Edited at: {message.edited_at}\n"
        f"Attachments: {[attachment.url for attachment in message.attachments]}\n" 
        )
    await message.channel.send(info_text)
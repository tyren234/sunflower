import discord

async def perform_help_message(message: discord.Message) -> None:
    help_text = (
        "\nAvailable commands:\n"
        "`!help` - Show this help message\n"
        "`!info` - Show info about this message\n"
        "`!count` - Count messages in the current channel\n"
        "`!save <message id>` - Save a specific message from this channel to a file\n"
        "`!save <message id> <channel id>` - Save a specific message from a specified channel to a file\n"
        "`!backup` - Backup all messages in the current channel to a file (doesn't work yet)\n"
    )
    await message.channel.send(help_text)
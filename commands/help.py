import discord

async def perform_help_message(message: discord.Message) -> None:
    help_text = (
        "\nAvailable commands:\n"
        "`!help` - Show this help message\n"
        "`!info <message id>` or `!info <message id> <channel id>` - Show info about message from specified channel\n"
        "`!count` - Count messages in the current channel\n"
        "`!save <message id>` or `!save <message id> <channel id>` - Save a specific message from a specified channel to a file. This will append the message to the end of the file.\n"
        "`!backup <channel id>` - Backup all messages in a specified channel to a file\n"
        "`!backupnew <channel id>` - Backup new messages in a specified channel since the last saved message\n"
        "`!last` - Show the last saved message ID from the current channel's backup file\n"
    )
    await message.channel.send(help_text)
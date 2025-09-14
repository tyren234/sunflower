# Overview

This is a discord bot serving to save messages from your discord server into selected local directory.
Made by [tyren234 a.k.a. flowerishman](https://github.com/tyren234).

# Commands

Currently available commands are:
- `!help` - Shows help message with list of commands
- `!info <message id>` or `!info <message id> <channel id>` - Show info about message
- `!count` - Count messages in the current channel
- `!save <message id>` or `!save <message id> <channel id>` - Save a specific message from a specified channel to a file
- `!backup <channel id>` - Backup all messages in a specified channel to a file
- `!backupnew <channel id>` - Backup new messages in a specified channel since the last saved message
- `!last` - Show the last saved message ID from the current channel's backup file

For upated list please see [help command source code](./commands/help.py).

# License

This software is free to use, but not to modify.
All rights reserved. Don't modify the software without explicit written permission. I'm more than happy to share the project, but please contact me. You can find me at tymonkwiat@gmail.com.
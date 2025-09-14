# Overview
This is a discord bot used to save messages from your discord server into selected local directory. It will save messages as markdown files, with attachments saved in a subdirectory. It can also backup all messages from a specified channel, or only new messages since the last saved message.

Most basic usecase is to have the bot running on your server and let it backup all the messages from your server as you send them.

# Setup
For the setup follow these steps:
1. Install [Python](https://www.python.org/downloads/). I used python 3.12.3.
2. Install required packages using pip. I'd recommend to use virtual environment:
    - you can use provided `requirements.txt` file:
        - `pip install -r requirements.txt`
    - or you can generate your own requirements file using pipreqs:
        - `pip install pipreqs`
        - `pipreqs . --force --ignore .venv,.vscode,__pycache__`
        - and then install packages using:
            - `pip install -r requirements.txt`
3. Create `.env` file in the root directory of the project. It serves as a configuration file. The most important part is to provide your discord bot token and the path to the directory where you want to save your messages. You can use `.env.example` file as a template. **Remember to never share your bot token with anyone!**
4. Run the bot using `python main.py`.

# Commands
Currently available commands are:
- `!help` - Shows help message with list of commands
- `!info <message id>` or `!info <message id> <channel id>` - Show info about message
- `!count` - Count messages in the current channel
- `!save <message id>` or `!save <message id> <channel id>` - Save a specific message from a specified channel to a file. This will append the message to the end of the file
- `!backup <channel id>` - Backup all messages in a specified channel to a file
- `!backupnew <channel id>` - Backup new messages in a specified channel since the last saved message
- `!last` - Show the last saved message ID from the current channel's backup file

You can also see that in [help command source code](./commands/help.py).

# License
This software is free to use, but not to modify.
All rights reserved. Don't modify the software without explicit written permission. I'm more than happy to share the project, but please contact me. You can find me at tymonkwiat@gmail.com.

# Author
Made by [tyren234 a.k.a. flowerishman](https://github.com/tyren234).
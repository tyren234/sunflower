import os
import discord
from dotenv import load_dotenv

sunflower_output_channel_id: str | None = None
sunflower_output_channel: discord.abc.Messageable | None = None

def load_output_channel_id() -> None:
    load_dotenv()

    global sunflower_output_channel_id
    sunflower_output_channel_id = os.getenv("SUNFLOWER_OUTPUT_CHANNEL_ID")
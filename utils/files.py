from pathlib import Path
import discord
import aiohttp
import aiofiles
from dotenv import load_dotenv
import os
import re

load_dotenv()
SUNFLOWER_SAVE_DIRECTORY: str | None = os.getenv("SUNFLOWER_SAVE_DIRECTORY")
if SUNFLOWER_SAVE_DIRECTORY is None:
    raise ValueError("No save directory found in environment variables.")
SUNFLOWER_FILE_EXTENSION: str | None = os.getenv("SUNFLOWER_FILE_EXTENSION")
if SUNFLOWER_FILE_EXTENSION is None:
    raise ValueError("No file extension found in environment variables.")
SUNFLOWER_ASSETS_DIRECOTORY_NAME: str | None = os.getenv("SUNFLOWER_ASSETS_DIRECOTORY_NAME")
if SUNFLOWER_ASSETS_DIRECOTORY_NAME is None:
    raise ValueError("No assets directory name found in environment variables.")

save_directory: Path = Path(SUNFLOWER_SAVE_DIRECTORY)
assets_directory: Path = save_directory / SUNFLOWER_ASSETS_DIRECOTORY_NAME
# This is relative to the notes file location
relative_assets_directory: Path = Path("..") / SUNFLOWER_ASSETS_DIRECOTORY_NAME

def get_save_path(server_name: str, channel_name: str, extension: str = SUNFLOWER_FILE_EXTENSION) -> Path:
    return Path(save_directory / server_name / channel_name).with_suffix(extension)

def get_asset_path(filename: str, name_prefix: str = "", relative_to_notes: bool = False) -> Path:
    if name_prefix:
        filename = f"{name_prefix}_{filename}"
    return (relative_assets_directory if relative_to_notes else assets_directory) / filename

async def download_attachments(attachments: list[discord.Attachment], name_prefix: str = "") -> list[Path]:
    '''
    Download attachments to the assets directory and return list of saved paths.

    Args:
        attachments (list[discord.Attachment]): List of attachments to download.
        name_prefix (str, optional): Prefix added to the filename. 

    Returns:
        list[Path]: List of local paths where attachments were saved.
    '''
    assets_directory.mkdir(exist_ok=True, parents=True)
    saved_paths: list[Path] = []

    for attachment in attachments:
        save_path = get_asset_path(attachment.filename, name_prefix)
        async with aiohttp.ClientSession() as session:
            async with session.get(attachment.url) as r:
                if r.status == 200:
                    async with aiofiles.open(save_path, "wb") as handler:
                        await handler.write(await r.read())
                        # Notes will contain relative paths that's why we use relative here
                        saved_paths.append(get_asset_path(attachment.filename, name_prefix, relative_to_notes=True))
    
    return saved_paths

def get_last_message_id_from_file(file_path: Path) -> tuple[str, int] | None:
    """
    Get the last saved message ID from the file.

    Args:
        file_path (Path): Path to the file.
        
    Returns:
        tuple[str, int] | None: Tuple of the last saved message header string and message ID, or `None` if file doesn't exist or no messages found."""
    if not file_path.exists():
        return None
    
    with file_path.open("r", encoding="utf-8") as file:
        content = file.read()
        # Match the exact header format: YYYY-MM-DD HH:MM:SS [message_id](https://...)
        matches = re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (\[(\d+)\]\(https:\/\/discord\.com\/channels\/\d+\/\d+\/\d+\))', content)
        if matches:
            return (matches[-1][0], int(matches[-1][1]))
    return None


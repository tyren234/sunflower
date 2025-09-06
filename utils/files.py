from pathlib import Path
from dotenv import load_dotenv
import os

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

def get_save_path(server_name: str, channel_name: str, extension: str = SUNFLOWER_FILE_EXTENSION) -> Path:
    return Path(save_directory / server_name / channel_name).with_suffix(extension)

def get_asset_path(filename: str) -> Path:
    return assets_directory / filename

# async def download_attachments(attachments: list) -> list[Path]:
#     """Download attachments to the assets directory and return list of saved paths."""
#     import aiohttp
    
#     assets_directory.mkdir(exist_ok=True, parents=True)
#     saved_paths = []
    
#     for attachment in attachments:
#         asset_path = get_asset_path(attachment.filename)
#         async with aiohttp.ClientSession() as session:
#             async with session.get(attachment.url) as r:
#                 if r.status == 200:
#                     async with aiofiles.open(asset_path, "wb") as handler:
#                         await handler.write(await r.read())
#                         saved_paths.append(asset_path)
    
#     return saved_paths


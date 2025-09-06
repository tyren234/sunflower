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

save_directory: Path = Path(SUNFLOWER_SAVE_DIRECTORY)
print(f"Using save directory: {save_directory}")

def get_save_path(server_name: str, channel_name: str, extension: str = SUNFLOWER_FILE_EXTENSION) -> Path:
    return Path(save_directory / server_name / channel_name).with_suffix(extension)
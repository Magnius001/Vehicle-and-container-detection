import glob
import os
import queue
from pathlib import Path
from typing import Callable

def load_images_from(path: str, image_exts: list[str] = ["png", "jpeg","jpg"]) -> list:
    all_images_file_names = []
    for ext in image_exts:
        found_files = glob.glob(os.path.join(path, f"*.{ext}"))
        all_images_file_names.extend(found_files)

    return all_images_file_names


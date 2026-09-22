import os
from pathlib import Path

def autoLoadPaths(folder_name: str = "src") -> list[str]:
    """
    Returns a list of fully qualified file paths in the given folder.
    Resolves relative to the project root (where this file lives),
    not the current working directory.
    """
    # Resolve base path relative to this file's directory
    project_root = Path(__file__).resolve().parents[0]  # adjust depth if needed
    base = project_root / folder_name

    if not base.exists():
        raise FileNotFoundError(f"Essay folder not found: {base}")

    return [
        str(base / f)
        for f in os.listdir(base)
        if (base / f).is_file()
    ]

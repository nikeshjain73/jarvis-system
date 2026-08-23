from pathlib import Path


def list_downloads():

    downloads = Path.home() / "Downloads"

    if not downloads.exists():
        return {
            "error": "Downloads folder not found."
        }

    files = []

    for item in downloads.iterdir():
        files.append({
            "name": item.name,
            "type": "folder" if item.is_dir() else "file"
        })

    return files
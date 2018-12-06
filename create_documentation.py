"""Script to create README files for a set of folders."""

from os import walk
from os.path import join

IGNORE_FOLDERS = ["__pycache__", "ignore_dir"]


def get_folders(base_dir=""):
    """
    Get folders and associated files from the directory.

    Args:
        base_dir (str): Directory to look at files in.

    Returns:
        FILL ME IN LATER

    """
    raise RuntimeError("DOOT: GET FOLDERS")


def parse_folders(folder_name):
    """
    Build documentation for the folder.

    Args:
        folder_name (str): Directory to parse.
    
    Returns:
        FILL ME IN LATER.
    """
    raise RuntimeError("DOOT PARSE FOLDERS")


def create_documentation():
    """Function to create documentation."""
    f = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        f.extend(filenames)
        break


if __name__ == "__main__":
    create_documentation()

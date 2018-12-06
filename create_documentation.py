"""Script to create README files for a set of folders."""

from os import listdir
from os.path import join, isfile, dirname, realpath

IGNORE_FOLDERS = ["__pycache__", "ignore_dir", ".git"]


def get_folders(base_dir=""):
    """
    Get folders and associated files from the directory.

    Args:
        base_dir (str): Directory to look at files in.

    Returns:
        FILL ME IN LATER

    """
    raise RuntimeError("DOOT: GET FOLDERS")


def parse_folder(folder_name):
    """
    Build documentation for the folder.

    Args:
        folder_name (str): Directory to parse.
    
    Returns:
        FILL ME IN LATER.
    """
    output = {}

    # Get list of folders to build documentation for
    folders = [file_ for file_ in listdir(folder_name) if not isfile(file_)]
    folders = [file_ for file_ in folders if file_ not in IGNORE_FOLDERS]

    files = [file_ for file_ in listdir(folder_name) if isfile(file_)]

    print(folders)
    print(files)

    raise RuntimeError("DOOT PARSE FOLDERS")
    return output



def create_documentation():
    """Function to create documentation."""
    current_dir = dirname(realpath(__file__))

    # Get the documentation for this (and all sub) directories
    file_info = parse_folder(current_dir)


if __name__ == "__main__":
    create_documentation()

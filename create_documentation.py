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
    folders = [file_ for file_ in listdir(folder_name) if not (isfile(file_) or ".py" in file_)]
    folders = [file_ for file_ in folders if file_ not in IGNORE_FOLDERS]

    files = [file_ for file_ in listdir(folder_name) if (isfile(file_) or ".py" in file_)]

    print("\n\nBASE: {}".format(folder_name))
    print("\tFOLDERS: {}".format(folders))
    print("\tFILES: {}".format(files))

    for sub_name in folders:
        output[sub_name] = parse_folder(join(folder_name, sub_name))

    return output


def create_documentation():
    """Function to create documentation."""
    current_dir = dirname(realpath(__file__))

    # Get the documentation for this (and all sub) directories
    file_info = parse_folder(current_dir)

    print(file_info)
    raise RuntimeError("DOOT PARSE FOLDERS")


if __name__ == "__main__":
    create_documentation()

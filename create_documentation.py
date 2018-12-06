"""Script to create README files for a set of folders."""

import ast

from os import listdir
from os.path import join, isfile, dirname, realpath

IGNORE_FOLDERS = ["__pycache__", "ignore_dir", ".git"]


def parse_file(file_name):
    """
    Get the documentation of the python file.

    Args:
        file_name (str): File name to parse.

    Returns:
        FILL ME IN LATER.

    """
    print("\nPARSING_FILE: {}".format(file_name))
    with open(file_name) as file_:
        code = ast.parse(file_.read())

    for node in ast.walk(code):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
            docstring = ast.get_docstring(node)
            if docstring:
                print(repr(docstring))


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

    files = [file_ for file_ in listdir(folder_name) if (".py" in file_)]

    print("\n\nBASE: {}".format(folder_name))
    print("\tFOLDERS: {}".format(folders))
    print("\tFILES: {}".format(files))

    for file_name in files:
        output[file_name] = parse_file(join(folder_name, file_name))

    for sub_name in folders:
        output[sub_name] = parse_folder(join(folder_name, sub_name))

    output["_folders"] = folders
    output["_files"] = files

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

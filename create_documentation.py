"""Script to create README files for a set of folders."""

import ast

from os import listdir
from os.path import join, isfile, dirname, realpath

IGNORE_FOLDERS = ["__pycache__", "ignore_dir", ".git"]


def parse_module(module_node):
    """Parse Module level node."""
    output = {}
    
    # Get Module docstring
    output["type"] = "module"
    output["docstring"] = repr(ast.get_docstring(module_node))
    output["class_children"] = []
    output["func_children"] = []

    for child_node in ast.iter_child_nodes(module_node):
        if isinstance(child_node, ast.ClassDef):
            output["class_children"].append(parse_class(child_node))
        elif isinstance(child_node, ast.FunctionDef):
            output["func_children"].append(parse_func(child_node))

    return output

def parse_class(class_node):
    """Parse Module level node."""
    print("CLASS")
    output = {}
    output["name"] = class_node.name
    output["type"] = "class"

    return output


def parse_func(func_node):
    """Parse Module level node."""
    output = {}
    output["name"] = func_node.name
    output["type"] = "func"

    return {}


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

    return parse_module(code)


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

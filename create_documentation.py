"""Script to create README files for a set of folders."""

import ast

from os import listdir
from os.path import join, isfile, dirname, realpath

import re

IGNORE_FOLDERS = ["__pycache__", "ignore_dir", ".git", "env", ".vscode"]


def parse_folder(folder_name):
    """
    Build documentation for the folder.

    Args:
        folder_name (str): Directory to parse.
    
    Returns:
        Dictionary with the docstring information for all files in that folder.

    """
    output = {}
    output["name"] = folder_name
    output["type"] = "folder"

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


def parse_file(file_name):
    """
    Get the documentation of the python file.

    Args:
        file_name (str): File name to parse.

    Returns:
        Dictionary with the information of the docstrings in the file.

    """
    print("\nPARSING_FILE: {}".format(file_name))
    with open(file_name) as file_:
        code = ast.parse(file_.read())
    output = parse_module(code)
    output["name"] = file_name

    return output


def parse_module(module_node):
    """
    Parse Module level node.

    Args:
        module_node (_ast.Module): AST Node for this module.

    Returns:
        Dictionary with the documentation info for this node.

    """
    output = {}

    # Get Module docstring
    output["type"] = "module"
    output["docstring"] = ast.get_docstring(module_node)
    output["class_children"] = []
    output["func_children"] = []

    for child_node in ast.iter_child_nodes(module_node):
        if isinstance(child_node, ast.ClassDef):
            output["class_children"].append(parse_class(child_node))
        elif isinstance(child_node, ast.FunctionDef):
            output["func_children"].append(parse_func(child_node))

    return output


def parse_class(class_node):
    """
    Parse Class level node.

    Args:
        module_node (_ast.ClassDef): AST Node for this class.

    Returns:
        Dictionary with the documentation info for this node.

    """
    print("CLASS: {}".format(class_node.name))

    output = {}
    output["name"] = class_node.name
    output["type"] = "class"
    output["docstring"] = ast.get_docstring(class_node)
    output["func_children"] = []

    for child_node in ast.iter_child_nodes(class_node):
        if isinstance(child_node, ast.FunctionDef):
            output["func_children"].append(parse_func(child_node))

    return output


def parse_func(func_node):
    """
    Parse Function level node.

    Args:
        module_node (_ast.FunctionDef): AST Node for this Function

    Returns:
        Dictionary with the documentation info for this node.

    """
    print("FUNCTION: {}".format(func_node.name))

    output = {}
    output["name"] = func_node.name
    output["type"] = "func"
    output["docstring"] = ast.get_docstring(func_node)

    return output


def build_files(file_info):
    """
    Actually build the documentation.
    
    Args:
        file_info (dict): All the directory info from earlier steps.

    """
    # print(file_info)
    # print(file_info.keys())

    output_str = ""

    print(file_info["name"], file_info["type"], file_info["_folders"], file_info["_files"])

    for file_name in file_info["_files"]:
        # Document files in the folder
        datum = file_info[file_name]
        print(datum)

        output_str = "{}# {}: {}\n".format(output_str, datum["type"] , file_name)
        if datum["docstring"]:
            output_str = "{}{}\n".format(output_str, datum["docstring"])

        for func_child in datum["func_children"]:
            output_str = "{}{}".format(output_str, build_docs_func(func_child))

    print(output_str)

    raise RuntimeError("DOOT PARSE FOLDERS")


def build_docs_func(func_info):
    """
    Build documentation for a function.
    
    Args:
        func_info (dict): Information about this function.

    """
    print("\n")
    print(func_info)
    out_str = "## Function: {}\n".format(func_info["name"])

    if func_info.get("docstring") and func_info["docstring"]:
        func_doc_arr = func_info["docstring"].split("\n\n")
        func_doc_arr = [val.strip() for val in func_doc_arr]

        out_str = "{}{}\n".format(out_str, func_doc_arr[0])

        arg_str = [docstr for docstr in func_doc_arr if docstr.startswith("Args:")]
        ret_str = [docstr for docstr in func_doc_arr if docstr.startswith("Returns:")]
        exc_str = [docstr for docstr in func_doc_arr if docstr.startswith("Raises:")]

        out_str = "{}#### Arguments:\n".format(out_str)
        if arg_str:
            arg_str = arg_str[0]
            args = [val.strip() for val in arg_str.split("\n")[1:]]
            for arg in args:
                name, type_, descr = re.search("(.+) \((.+)\): (.+)", arg).groups()
                print(arg)
                print(name, type_, descr)
                out_str = "{out_str}- {name}\n  - Type: {type}\n  - {descr}\n".format(
                    out_str=out_str,
                    name=name,
                    type=type_,
                    descr=descr
                )
        else:
            out_str = "{}_None_\n".format(out_str)

        out_str = "{}#### Returns:\n".format(out_str)
        if ret_str:
            ret_str = ret_str[0].replace("Returns:\n","").strip()
            out_str = "{}{}\n".format(out_str, ret_str)
        else:
            out_str = "{}_None_\n".format(out_str)

    out_str = "{}\n".format(out_str)
    return out_str


def create_documentation():
    """Function to create documentation."""
    current_dir = dirname(realpath(__file__))

    # Get the documentation for this (and all sub) directories
    file_info = parse_folder(current_dir)
    build_files(file_info)


if __name__ == "__main__":
    create_documentation()

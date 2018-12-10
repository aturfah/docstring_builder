"""Script to create README files for a set of folders."""

import ast

from os import listdir
from os.path import join, isfile, dirname, realpath

import re

IGNORE_FOLDERS = ["__pycache__", "ignore_dir", ".git", "env", ".vscode"]

ARGUMENT_ALIASES = ["Args:", "Arguments:"]
RETURNS_ALIASES = ["Returns:"]
EXCEPTION_ALIASES = ["Raises:"]
ALL_ALIASES = ARGUMENT_ALIASES + RETURNS_ALIASES + EXCEPTION_ALIASES

OUTPUT_FILENAME = "DOCUMENTATION.md"

def test_func(arg1, arg2):
    """
    Test function for documentation.

    Here is a more detailed description of the function and
    what it does.

    Args:
        arg1 (type1): Description of arg1.
        arg2 (type2): Description of arg2 that spans multiple lines
            like the so.

    Returns:
        Description of what this returns.

    """
    pass


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

    # print("\n\nBASE: {}".format(folder_name))
    # print("\tFOLDERS: {}".format(folders))
    # print("\tFILES: {}".format(files))

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
    # print("\nPARSING_FILE: {}".format(file_name))
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
    # print("CLASS: {}".format(class_node.name))

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
    # print("FUNCTION: {}".format(func_node.name))

    output = {}
    output["name"] = func_node.name
    output["type"] = "func"
    output["docstring"] = ast.get_docstring(func_node)

    output["docstring"] = output["docstring"].replace("<", "\<")
    output["docstring"] = output["docstring"].replace(">", "\>")

    return output


def build_files(file_info, base_path):
    """
    Actually build the documentation.
    
    Args:
        file_info (dict): All the directory info from earlier steps.

    """
    # Build header
    module_name = file_info["name"].replace(base_path, "")
    if "\\" in module_name:
        module_name = module_name.replace("\\", "")
    if not module_name:
        module_name = "Base Directory"
    output_str = "# Module: `{}`\n".format(module_name)

    # Make sure that the __init__.py is at the front
    try:
        init_ind = file_info["_files"].index("__init__.py")
        del file_info["_files"][init_ind]
        file_info["_files"] = ["__init__.py"] + file_info["_files"]
    except ValueError:
        pass

    for file_name in file_info["_files"]:
        # Document files in the folder
        datum = file_info[file_name]

        output_str = "{}## File: `{}`\n".format(output_str, file_name)
        if datum["docstring"]:
            output_str = "{}{}\n".format(output_str, datum["docstring"])

        for func_child in datum["func_children"]:
            output_str = "{}{}".format(output_str, build_docs_func(func_child))

        for class_child in datum["class_children"]:
            output_str = "{}{}".format(output_str, build_docs_class(class_child))

    if file_info["_folders"]:
        output_str = "{}## Subdirectory Links:\n".format(output_str)
        for folder_name in file_info["_folders"]:
            # Create documentation for files in folder
            datum = file_info[folder_name]
            build_files(datum, file_info["name"])

            # Add Subdir links
            subdir_link = join(datum["name"].replace(base_path, ""), OUTPUT_FILENAME)
            if subdir_link.startswith("\\"):
                subdir_link = subdir_link[1:]

            output_str = "{output_str}- [{folder_name}]({link})\n".format(
                output_str=output_str,
                folder_name=datum["name"].replace(base_path, ""),
                link=subdir_link
            )

    with open(join(file_info["name"], OUTPUT_FILENAME), 'w') as out_file:
        out_file.write(output_str)


def arr_startswith(input_str, match_arr):
    """
    Test if string starts with any member of array.

    Arguments:
        input_str (str): String to check against.
        match_arr (list): List of items to check for.

    Returns:
        True if input_str starts with amy member of match_arr

    """
    for item in match_arr:
        if input_str.startswith(item):
            return True

    return False


def build_docs_func(func_info):
    """
    Build documentation for a function.
    
    Args:
        func_info (dict): Information about this function.

    """
    out_str = "### Function: `{}`\n".format(func_info["name"])

    if func_info.get("docstring") and func_info["docstring"]:
        func_doc_arr = func_info["docstring"].split("\n\n")
        func_doc_arr = [val.strip() for val in func_doc_arr]

        arg_str = [docstr for docstr in func_doc_arr if arr_startswith(docstr, ARGUMENT_ALIASES)]
        ret_str = [docstr for docstr in func_doc_arr if arr_startswith(docstr, RETURNS_ALIASES)]
        exc_str = [docstr for docstr in func_doc_arr if arr_startswith(docstr, EXCEPTION_ALIASES)]
        other_str = [docstr for docstr in func_doc_arr if not arr_startswith(docstr, ALL_ALIASES)]

        # Build function description 
        if other_str:
            out_str = "{}{}\n".format(out_str, other_str[0])
            other_str = [val.replace("\n", " ") for val in other_str]
            if len(other_str) > 1:
                out_str = "{}\n#### Description\n{}\n".format(out_str, " ".join(other_str[1:]))

        # Build documentation for Arguments
        out_str = "{}#### Arguments:".format(out_str)
        if arg_str:
            arg_str = arg_str[0]
            args = [val.strip() for val in arg_str.split("\n")[1:]]
            for arg in args:
                matching = re.search("(.+) \((.+)\): (.+)", arg)
                if matching is not None:
                    name, type_, descr = matching.groups()
                    out_str = "{out_str}\n- {name}\n  - Type: {type}\n  - {descr}".format(
                        out_str=out_str,
                        name=name,
                        type=type_,
                        descr=descr.strip()
                    )
                else:
                    out_str = "{out_str} {descr_cont}".format(
                        out_str=out_str,
                        descr_cont=arg.strip()
                    )
            out_str = "{}\n".format(out_str)
        else:
            out_str = "{}\n_None_\n".format(out_str)

        # Build documentation for Returns
        out_str = "{}#### Returns:\n".format(out_str)
        if ret_str:
            ret_str = ret_str[0].replace("Returns:\n","").strip()
            out_str = "{}{}\n".format(out_str, ret_str)
        else:
            out_str = "{}_None_\n".format(out_str)

        # TODO: Add exceptions

    out_str = "{}\n".format(out_str)
    return out_str


def build_docs_class(class_info):
    """
    Build documentation for a class.
    
    Args:
        class_info (dict): Information about this class.

    """
    out_str = "### Class: `{}`\n".format(class_info["name"])

    if class_info.get("docstring"):
        out_str = "{}{}\n".format(out_str, class_info["docstring"])

    for func_child in class_info["func_children"]:
        out_str = "{}{}".format(out_str, build_docs_func(func_child))

    # print(class_info)
    return out_str


def create_documentation():
    """Function to create documentation."""
    current_dir = dirname(realpath(__file__))

    # Get the documentation for this (and all sub) directories
    file_info = parse_folder(current_dir)
    build_files(file_info, current_dir)


if __name__ == "__main__":
    create_documentation()

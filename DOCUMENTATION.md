# Module: `Base Directory`
## File: `create_documentation.py`
Script to create README files for a set of folders.
### Function: `test_func`
Test function for documentation.

#### Description
Here is a more detailed description of the function and what it does.
#### Arguments:
- arg1
  - Type: type1
  - Description of arg1.
- arg2
  - Type: type2
  - Description of arg2 that spans multiple lines like the so.
#### Returns:
Description of what this returns.

### Function: `parse_folder`
Build documentation for the folder.
#### Arguments:
- folder_name
  - Type: str
  - Directory to parse.
#### Returns:
Dictionary with the docstring information for all files in that folder.

### Function: `parse_file`
Get the documentation of the python file.
#### Arguments:
- file_name
  - Type: str
  - File name to parse.
#### Returns:
Dictionary with the information of the docstrings in the file.

### Function: `parse_module`
Parse Module level node.
#### Arguments:
- module_node
  - Type: _ast.Module
  - AST Node for this module.
#### Returns:
Dictionary with the documentation info for this node.

### Function: `parse_class`
Parse Class level node.
#### Arguments:
- module_node
  - Type: _ast.ClassDef
  - AST Node for this class.
#### Returns:
Dictionary with the documentation info for this node.

### Function: `parse_func`
Parse Function level node.
#### Arguments:
- module_node
  - Type: _ast.FunctionDef
  - AST Node for this Function
#### Returns:
Dictionary with the documentation info for this node.

### Function: `build_files`
Actually build the documentation.
#### Arguments:
- file_info
  - Type: dict
  - All the directory info from earlier steps.
#### Returns:
_None_

### Function: `arr_startswith`
Test if string starts with any member of array.
#### Arguments:
- input_str
  - Type: str
  - String to check against.
- match_arr
  - Type: list
  - List of items to check for.
#### Returns:
True if input_str starts with amy member of match_arr

### Function: `build_docs_func`
Build documentation for a function.
#### Arguments:
- func_info
  - Type: dict
  - Information about this function.
#### Returns:
_None_

### Function: `build_docs_class`
Build documentation for a class.
#### Arguments:
- class_info
  - Type: dict
  - Information about this class.
#### Returns:
_None_

### Function: `create_documentation`
Function to create documentation.
#### Arguments:
_None_
#### Returns:
_None_

## Subdirectory Links:
- [\dir1](\dir1\DOCUMENTATION.md)
- [\dir2](\dir2\DOCUMENTATION.md)
- [\dir3](\dir3\DOCUMENTATION.md)

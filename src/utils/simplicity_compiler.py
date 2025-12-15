"""
SimplicityHL Compilation Utilities

Provides wrapper functions for pysimplicityhl compilation
with proper file handling and error reporting.
"""

import json
import tempfile
import os
import platform
import traceback
from typing import Dict, Any, Tuple, Optional


def create_temp_file(suffix: str = "", directory: Optional[str] = None, 
                     delete: bool = True) -> Tuple[str, Any]:
    """
    Create a temporary file with a user-defined suffix and directory.

    Args:
        suffix: File extension, e.g. ".txt" or ".simf"
        directory: Directory where the file should be created
        delete: If True, file is deleted when closed

    Returns:
        Tuple of (filename, file_object)
    """
    if not suffix.startswith("."):
        suffix = f".{suffix}"
    
    tmp = tempfile.NamedTemporaryFile(
        suffix=suffix,
        dir=directory,
        delete=delete
    )
    
    return tmp.name, tmp


def write_text_to_temp_file(text: str, suffix: str = "", 
                           directory: Optional[str] = None) -> str:
    """
    Create a temporary file, write text into it, return filename.

    Args:
        text: The text content to write
        suffix: File extension
        directory: Directory where file will be created

    Returns:
        Full path of created temporary file
    """
    filename, f = create_temp_file(suffix=suffix, directory=directory, delete=False)
    
    f.write(text.encode("utf-8"))
    f.flush()
    f.close()
    
    return filename


def compile_simplicity(code: str, witness: Optional[str] = None, 
                      folder: Optional[str] = None, 
                      delete_temp_files: bool = True) -> Dict[str, Any]:
    """
    Compile SimplicityHL using pysimplicityhl.

    Args:
        code: SimplicityHL source code (or file path)
        witness: Witness data as JSON string (or file path)
        folder: Working folder for temp files
        delete_temp_files: Delete temp files after compilation

    Returns:
        Dictionary with compilation results
    """
    
    try:
        import pysimplicityhl
    except ImportError:
        return {
            "status": "error",
            "message": "pysimplicityhl not installed",
            "error": True
        }
    
    res = {}
    _temp_folder = "."
    
    # Determine working folder
    if folder is not None:
        if not os.path.exists(folder):
            res["warning"] = f"Folder does not exist, using default: {_temp_folder}"
        else:
            _temp_folder = folder
    
    # Handle code file
    cfile_given = False
    if code is not None and os.path.isfile(code):
        simf_file = code
        cfile_given = True
    elif code is None:
        res["error"] = True
        res["status"] = "error"
        res["message"] = "Code is empty or file does not exist"
        return res
    else:
        simf_file = write_text_to_temp_file(code, suffix="simf", directory=_temp_folder)
    
    # Handle witness file
    wit_file = None
    wfile_given = False
    if witness is not None and os.path.isfile(witness):
        wfile_given = True
        wit_file = witness
    elif witness is not None:
        wit_file = write_text_to_temp_file(witness, suffix="wit", directory=_temp_folder)
    
    # Detect Windows
    is_windows = platform.system().lower().startswith("win")
    
    # Build parameter list
    parameter = ["--debug"]
    parameter.append(f"'{simf_file}'" if is_windows else simf_file)
    if wit_file is not None:
        parameter.append(f"'{wit_file}'" if is_windows else wit_file)
    
    parameter_txt = " ".join(parameter)
    
    try:
        # Run compilation
        result_json = pysimplicityhl.run_from_python(parameter_txt)
        result = json.loads(result_json)
        res.update(result)
        
    except Exception as e:
        res["error"] = True
        res["status"] = "error"
        res["message"] = f"Compilation exception: {str(e)}"
        res["traceback"] = traceback.format_exc()
        res["code_file"] = simf_file
        res["witness_file"] = wit_file
        return res
    
    # Handle deletion of temp files
    if delete_temp_files:
        try:
            if os.path.isfile(simf_file) and not cfile_given:
                os.remove(simf_file)
            if wit_file and os.path.isfile(wit_file) and not wfile_given:
                os.remove(wit_file)
        except Exception as e:
            res["warning"] = f"Failed to delete temp files: {str(e)}"
            res["code_file"] = simf_file
            res["witness_file"] = wit_file
            res["deleted"] = False
        return res
    
    # If not deleting, store filenames
    res["code_file"] = simf_file
    res["witness_file"] = wit_file
    res["deleted"] = False
    return res


def pretty_print_code(code: str, indent_step: int = 2) -> str:
    """
    Pretty-print a nested expression string.

    Args:
        code: Code to format
        indent_step: Indentation step size

    Returns:
        Formatted code
    """
    indent = 0
    i = 0
    n = len(code)
    result = ""
    
    while i < n:
        c = code[i]
        if c == '(':
            result += '('
            indent += indent_step
            i += 1
        elif c == ')':
            indent -= indent_step
            result += ')'
            i += 1
        elif c == ';':
            result += ';\n' + ' ' * indent
            i += 1
        else:
            result += c
            i += 1
    
    return '\n'.join(line.rstrip() for line in result.split('\n'))

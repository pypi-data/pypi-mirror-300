"""Module that aims to analyze a whole package based 
on the other unitary function of the package"""

from loguru import logger
from tucan.unformat_main import unformat_main
from tucan.struct_main import struct_main
from tucan.tucanexceptions import TucanError


def run_unformat(clean_paths: list) -> dict:
    """
    Gather the unformated version of code files within a dict.

    Args:
        clean_paths (list): List of cleaned paths.

    Returns:
        dict: File path as key, item as a list of lines with their line number span
    """
    statements = {}
    for file in clean_paths:
        statements[file] = unformat_main(file).to_nob()

        nbr_of_stmt = 0
        if statements[file]:
            nbr_of_stmt = len(statements[file])
        logger.info(f"Found {nbr_of_stmt} statements for {file}")

    return statements


def run_struct(all_paths: dict, ignore_errors:bool=True, only_procedures=False) -> dict:
    """
    Gather the data associated to the functions within a file.

    Args:
        clean_paths (list): List of cleaned paths.

    Returns:
        dict: File path as key, item as dict with function names and their data (NLOC, CCN, etc.)
    """
    full_struct = {}
    files = []

    #files = clean_extensions_in_paths(files)
    for file, path in all_paths.items():
        try:
            struct = struct_main(path)

            if only_procedures: 
                to_remove=[]
                for part, data in struct.items():
                    if data["type"] in ["file"]:
                        to_remove.append(part)
                for part in to_remove:
                    del struct[part]

            full_struct[file] = struct

        except TucanError:
            logger.warning(f"Struct analysis failed on {file}")
            if ignore_errors:
                full_struct[file] = {}
            else:
                userinput = input("Would you like to continue (y/n)?")
                if userinput == "y":
                    full_struct[file] = {}
                else:
                    raise # raise previous error

    return full_struct

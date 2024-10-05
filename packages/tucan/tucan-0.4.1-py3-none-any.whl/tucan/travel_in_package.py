
from pathlib import Path
import os
from glob import glob
from ctypes import c_int64  # amutable int
from loguru import logger

from tucan.supported_files import ALL_SUPPORTED_EXTENSIONS


def find_package_files_and_folders(path: str,
    optional_paths: list = None,
)-> dict:
    paths = _rec_travel_through_package(path,optional_paths=optional_paths)
    return  _get_package_files(paths,path)

def _rec_travel_through_package(
    path: str,
    optional_paths: list = None,
) -> list:
    """
    List all paths from a folder and its sub-folders recursively.

    RECURSIVE
    """
    if not optional_paths:
        optional_paths = []

    current_paths_list = [path, *optional_paths]

    # Move to absolute Path objects
    current_paths_list = [Path(p_) for p_ in current_paths_list]
   
    paths_ = []
    for current_path in current_paths_list:
        for element in current_path.iterdir():
            
            if element.is_dir():
                path_str = element.as_posix()
                paths_.extend(_rec_travel_through_package(path_str))
            else:
                if not element.as_posix().endswith(ALL_SUPPORTED_EXTENSIONS):
                    continue
                if element.as_posix() not in paths_:
                    if not element.as_posix().split("/")[-1].startswith("."):
                        paths_.append(element.as_posix())
           
    return paths_


def _get_package_files(clean_paths: list, relpath: str) -> dict:
    """
    Return all the files useful for a package analysis, with their absolut paths

    """

    files = []
    for path_ in clean_paths:
        if not Path(path_).is_dir():
            #            logger.info(f"Append :{path_}")
            files.append(path_)

    files = _clean_extensions_in_paths(files)

    if not files:
        logger.warning(f"No files found in the paths provided")

    files = [ Path(p_) for p_ in files]

    out = {}
    for file in files:
        path_ = file.relative_to(Path(relpath)).as_posix()
        out[path_] = file.as_posix()
        
    return out


def _clean_extensions_in_paths(paths_list: list) -> list:
    """
    [PRIVATE] Remove unwanted path extensions and duplicates.

    Args:
        paths_list (list): List of all paths gatheres through recursive analysis

    Returns:
        list: List of cleaned paths.
    """
    clean_paths = []
    for path in paths_list:
        if path.endswith(ALL_SUPPORTED_EXTENSIONS):
            clean_paths.append(path)
        
    return [
        *set(clean_paths),
    ]




def scan_wdir(wdir):
    """ Build the structure of a folder tree.

    :params wdir: path to a directory
    """
    def _rec_subitems(path:str):#, item_id):
        file = Path(path)

        type_="folder"
        if file.is_file():
            type_="file"
            if file.suffix not in ALL_SUPPORTED_EXTENSIONS:
                return None
        out = {
            "name": file.name,
            "relpath": file.relative_to(Path(wdir)).as_posix(),
            "type": type_
        }
        
        if file.is_dir():
            out["children"] = list()
            for nexpath in glob(os.path.join(path, "**")):
                record = _rec_subitems(nexpath)
                if record is not None:
                    out["children"].append(record)
        return out
    
    out = _rec_subitems(wdir)#, 0, item_id=c_int64(-1))]

    return out

import os as __os
import sys as __sys

#This funcion is similar to: filefind(fn, path_dirs) de IPython.utils.path
def find_in_paths(fn: str, paths: list[str]):
  """Find a file with the specified name in a list of directories.

  This function searches for a file with the given filename in a list of directories.
  It returns a list of paths where the file is found.

  Parameters:
      fn (str): The name of the file to search for.
      paths (list[str]): A list of directory paths to search in.

  Returns:
      list: A list of paths where the file is found.

  Usage:
      find_in_paths("example.txt", ["/path1", "/path2", "/path3"])
  """
  return [__os.path.join(p, fn) for p in paths if __os.path.exists(__os.path.join(p, fn))]


def sys_paths (fn: str,
              sys_search: bool = True,
              os_search: bool = True,
              sys_first: bool = True):
  """Search for a file in system and environment paths.

  This function searches for a file in both system and environment paths.
  You can specify whether to search in system paths, environment paths, and
  whether to prioritize system paths over environment paths.

  Parameters:
      fn (str): The name of the file to search for.
      sys_search (bool, optional): If True, search in system paths. Default is True.
      os_search (bool, optional): If True, search in environment paths. Default is True.
      sys_first (bool, optional): If True, prioritize system paths. Default is True.

  Returns:
      list: A list of paths where the file is found.

  Usage:
      sys_paths("example.txt", sys_search=True, os_search=True, sys_first=True)
  """
  spath = __sys.path if sys_search else ["."]
  opath = __os.environ["PATH"].split(__os.pathsep) if os_search else ["."]
  paths = remove_copies (spath + opath if sys_first else opath + spath)

  return find_in_paths(fn, paths)


def add2syspath(folder:str, add2sys: bool = True, add2env: bool = True):
  """Add a folder to the system's module search path.

  This function allows you to add a specific folder to the system's module search path (sys.path).
  If the folder is not already in the path, it will be appended.

  Parameters:
    folder (str): The path of the folder to be added to the system's module search path.

  Example:
    add2syspath("/path/to/your/folder")
  """
  full_path = __os.path.abspath(folder)
  if add2sys and full_path not in __sys.path:
    __sys.path.append(full_path)
  if add2env and not full_path in __os.environ['PATH'].split(":"):
    __os.environ['PATH']=f"{__os.environ['PATH']}:{full_path}"
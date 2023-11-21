#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Script for downloading scripts and extensions to run R/exams in Google Colab.

This script downloads script and extension files from a Git repository and can
perform additional actions such as changing script file permissions and loading
extensions.

Usage:
  1. %run download_sripts_and_extensions [arguments]
  2. %sysrun download_sripts_and_extensions [arguments] # if already downloaded

  Not recommended options
  3. !python download_sripts_and_extensions.py [arguments]
  4. !chmod -x download_sripts_and_extensions.py  #run it onces
     !./download_sripts_and_extensions.py [arguments]

Arguments:
  --no-scripts, -ns:
      Exclude script downloads.
  --no-extension, -ne:
      Exclude extension downloads.
  --preserve-script-permissions, -psp:
      Preserve execution permissions for script files. Ignoder if `--no-scripts`.
  --no-load-extensions, -nld:
      Skip loading previously downloaded extensions. Ignoder if `--no-extension`.


Example Usage:
  %run download_sripts_and_extensions.py --no-scripts
  %run download_sripts_and_extensions.py --no-extension --preserve-script-permissions
  %run download_sripts_and_extensions --no-load-extensions

For more details and usage instructions, please refer to the script's
repository and the R/exams documentation.
  * [RExamsUtils](https://github.com/Mr-McGL/RExamsUtils)

ToDo:
  * PATH DOES NOT WORK!!!! REMOVE?
  * PERMISSION DO NOT WORK!!!! REMOVE?
  * ADD DEPENDENCIES

Additional Info
  @Author: Marcos García-Lorenzo
  @Maintainer:Marcos García-Lorenzo
  @e-mail: marcos.garcia@urjc.es

  @Version: 0.1.0
  @Date Created: October 19th, 2023
  @Date Modified: November 19, 2023
  @Status: 2 - Pre-Alpha

  @Copyright: © 2023 by Marcos García-Lorenzo (VGLAB - MIMIC - URJC). All rights reserved.
  @License: MIT License
"""
# @Links: {'MIMIC': 'https://gestion2.urjc.es/pdi/grupos-innovacion/mimic', 'VG-LAB': 'https://vg-lab.es/', 'URJC': 'https://www.urjc.es', 'R/exams': 'https://www.r-exams.org/', 'Project-URL': 'https://github.com/Mr-McGL/RExamsUtils'}

__metadata__ = dict(
		__name__ = "download_sripts_and_extensions",
		__project_name__ = "RExamsUtils",
		__keywords__ = ['Jupyter', 'Google Colab', 'R/exams'],
		__description__ = "Script for downloading scripts and extensions to run R/exams in Google Colab.",
		__version__ = "0.1.0",
		__date_created__ = "October 19th, 2023",
		__date_modified__ = "November 19, 2023",
		__status__ = "2 - Pre-Alpha",
		__license__ = {'text': 'MIT License'},
		__copyright__ = "© 2023 by Marcos García-Lorenzo (VGLAB - MIMIC - URJC). All rights reserved.",
		__authors__ = [{'name': 'Marcos García-Lorenzo', 'email': 'marcos.garcia@urjc.es'}],
		__maintainers__ = [{'name': 'Marcos García-Lorenzo', 'email': 'marcos.garcia@urjc.es'}],
		__contributors__ = "N.A.",
		__credits__ = "N.A.",
		__classifiers__ = ['Programming Language :: Python :: 3', 'License :: OSI Approved :: MIT License', 'Intended Audience :: Education', 'Development Status :: 2 - Pre-Alpha'],
		__dependencies__ = "N.A.",
		__requires_python__ = "N.A.",
		__urls__ = {'MIMIC': 'https://gestion2.urjc.es/pdi/grupos-innovacion/mimic', 'VG-LAB': 'https://vg-lab.es/', 'URJC': 'https://www.urjc.es', 'R/exams': 'https://www.r-exams.org/', 'Project-URL': 'https://github.com/Mr-McGL/RExamsUtils'})

import requests
import json

import os
import sys
import subprocess
from IPython import get_ipython

import argparse

#---

def reload_ext(ext: str):
  """Reload a Jupyter notebook extension.

  This function reloads a Jupyter notebook extension, allowing you to update
  the extension without restarting the kernel.

  Parameters:
      ext (str): The name of the extension to be reloaded.

  Usage:
      reload_ext("rpy2")
  """
  get_ipython().run_line_magic('reload_ext', ext)

#---

def run (cmd: str, olst: bool = False, raise_on_error: bool = True):
  """Run a shell command in the Jupyter notebook.

  This function allows you to run a shell command in the Jupyter notebook. You
  can capture the command's output, print it, and raise an error if the command
  returns a non-zero exit code.

  Parameters:
      cmd (str): The shell command to be executed.
      olst (bool, optional): If True, capture the command's output as a list of lines.
          If False, print the output to the notebook. Default is False.
      raise_on_error (bool, optional): If True, raise an error if the command returns
          a non-zero exit code. If False, do not raise an error. Default is True.

  Returns:
      If olst is True, returns a list of lines from the command's output.
      If olst is False, returns None.

  Raises:
      OSError: If raise_on_error is True and the command returns a non-zero exit code.

  Usage:
      run("ls -l", olst=True, raise_on_error=True)
  """
  if raise_on_error:
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    if not olst: print(proc.stdout)
    if proc.returncode !=0: raise OSError(proc)

    if olst:  return proc.stdout
    else: return

  #Ipython code for !
  elif olst:
    return get_ipython().getoutput(cmd)

  #Ipython code for !
  else:
    get_ipython().system(cmd)

#---

def download_git_file(user: str, repo: str, repo_folder: str, name: str,
                        server: str = "github.com",
                        branch: str = "main",
                        folder: str | None = None):
  """Download a file from a Git repository hosted on a Git server.

  This function allows you to download a specific file from a Git repository
  hosted on a Git server. You can specify the user, repository name, repository
  folder, file name, and other optional parameters.

  Parameters:
      user (str): The username or organization name that owns the Git repository.
      repo (str): The name of the Git repository.
      repo_folder (str): The path to the folder in the repository where the file is located.
      name (str): The name of the file to download.
      server (str, optional): The Git server hostname. Default is "github.com".
      branch (str, optional): The Git branch where the file is located. Default is "main".
      folder (str | None, optional): The local folder where the file will be saved.
          If None, the file is saved in the current working directory. Default is None.

  Raises:
      RequestException: If the file retrieval fails.

  Usage:
      download_git_file("username", "repository_name", "folder/path", "file.txt")
  """

  if folder is None: folder = "."

  file_url = f"https://{server}/{user}/{repo}/raw/{branch}/{repo_folder}/{name}"

  resp = requests.get(file_url)
  if resp.status_code != 200:
    raise requests.exceptions.RequestException(
      f"Failed to retrieve file ({repo_folder}/{name}). Status code: {resp.status_code}")

  with open(f"{folder}/{name}","wb") as f:
    f.write(resp.content)

#---

def download_git_folder(user: str, repo: str, repo_folder: str,
                        server: str = "github.com",
                        branch: str = "main",
                        folder: str | None = None):
  """Download all files from a folder in a Git repository hosted on a Git server.

  This function allows you to download all the files from a specific folder in
  a Git repository hosted on a Git server. You can specify the user, repository
  name, repository folder, and other optional parameters. The folders will
  be added to the path.

  Parameters:
      user (str): The username or organization name that owns the Git repository.
      repo (str): The name of the Git repository.
      repo_folder (str): The path to the folder in the repository to download.
      server (str, optional): The Git server hostname. Default is "github.com".
      branch (str, optional): The Git branch where the folder is located. Default is "main".
      folder (str | None, optional): The local folder where the files will be saved.
          If None, the files are saved in the current working directory. Default is None.

  Raises:
      RequestException: If the folder retrieval fails.

  Usage:
      download_git_folder("username", "repository_name", "folder/path")
  """

  if folder is None: folder = "."

  folder_url = f"https://{server}/{user}/{repo}/blob/{branch}/{repo_folder}"

  resp = requests.get(folder_url)
  if resp.status_code != 200:
      raise requests.exceptions.RequestException(
        f"Failed to retrieve folder({repo_folder}). Status code: {resp.status_code}")

  items = json.loads(resp.content)["payload"]["tree"]["items"]

  os.makedirs(folder, exist_ok=True)
  for item in items:
    if item['contentType'] == 'file':

      download_git_file(user, repo, repo_folder, item['name'],
                        server = server, branch = branch, folder = folder)

    else:
      download_git_folder(user, repo, f"{repo_folder}/{item['name']}",
                          server = server, branch = branch,
                          folder = f"{folder}/{item['name']}")

def add2syspath(folder:str):
  """Add a folder to the system's module search path.

  This function allows you to add a specific folder to the system's module search path (sys.path).
  If the folder is not already in the path, it will be appended.

  Parameters:
    folder (str): The path of the folder to be added to the system's module search path.

  Example:
    add2syspath("/path/to/your/folder")
  """
  full_path = os.path.abspath(folder)
  if full_path not in sys.path:
    sys.path.append(full_path)
  if not full_path in os.environ['PATH'].split(":"):
    os.environ['PATH']=f"{os.environ['PATH']}:{full_path}"

if __name__ == '__main__':

  ap = argparse.ArgumentParser(description = "Download scripts and extensions for running R/exams in Google Colab.")

  ap.add_argument('--no-scripts', '-ns', dest='download_scripts', action='store_false',
                  help="Exclude script downloads.")
  ap.add_argument('--no-extension', '-ne', dest='download_ext', action='store_false',
                  help="Exclude extension downloads.")
  ap.add_argument('--preserve-script-permissions', '-psp',
                  dest='change_permissions', action='store_false',
                  help="Preserve execution permissions for script files")
  ap.add_argument('--no-load-extensions', '-nld',
                  dest='load_extensions', action='store_false',
                  help="Skip loading previously downloaded extensions.")

  ap.set_defaults(download_scripts=True, download_ext=True,
                  change_permissions=True, load_extensions=True)

  args = ap.parse_args()

  swd = get_ipython().starting_dir
  script_folder = f"{swd}/scripts"
  ext_folder = f"{swd}/extensions"
  py_file_extensions = [".py", ".PY", ".ipynb", ".IPYNB"]

  if args.download_scripts:
    print(f"\x1B[1m\x1B[4m\x1b[34m\nDownloading scripts...\x1b[0m", flush=True)
    download_git_folder("Mr-McGL", "RExamsUtils", "nbscripts",
                      branch="dev/mgarcia", folder = script_folder)
    add2syspath(script_folder)

    if args.change_permissions:
      print(f"\x1B[1m\x1B[4m\x1b[34m\nUpdating permissions for script files...\x1b[0m", flush=True)
      for ext in py_file_extensions:
        if len([f for f in os.listdir(script_folder) if f.endswith(ext)]) != 0:
          run(f"chmod +x {script_folder}/*{ext}")
          run(f"ls -l {script_folder}/*{ext}")

  if args.download_ext:
    print(f"\x1B[1m\x1B[4m\x1b[34m\nDownloading extensions...\x1b[0m", flush=True)
    download_git_folder("Mr-McGL", "RExamsUtils", "nbext",
                      branch="dev/mgarcia", folder = ext_folder)
    add2syspath(ext_folder)

    if args.load_extensions:
      print(f"\x1B[1m\x1B[4m\x1b[34m\nLoading extensions...\x1b[0m", flush=True)
      for f in os.listdir(ext_folder):
        if any(f.endswith(ext) for ext in py_file_extensions):
          print(f"* \x1b[32m{f}\x1b[0m", flush=True)
          reload_ext(os.path.splitext(f)[0])

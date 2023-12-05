#!/usr/bin/env python
# -*- coding: utf-8 -*-

#__doc__ =
"""This script installs the R/exams package and its dependencies for use in Jupyter Notebooks via 'rpy2'.

  This script installs the R/exams package, which is a powerful tool for
  creating exams in R, for its use in Jupyter Notebooks via 'rpy2'.
  This script provides various options to customize the installation process

  Usage:

    1. %run init_rexams [arguments]
    2. %sysrun init_rexams [arguments]

    Not recommended options
    3. !python init_rexams.py [arguments]
    4. !chmod -x init_rexams.py  #run it onces
       !./init_rexams.py [arguments]

  Arguments:
    --rpy2ver, -rv <version>:
        Specify the version of 'rpy2' to use. *Defaults to None.*
    --demo-path, -dp <path>:
        Specify the installation path for R/exams demo files. *Defaults to None.*
    --rdev, -rd:
        Install the development version of R/exams (not recommended).
    --no-nops-support, -nns:
        Exclude support for NOPS.
    --no-pypandoc, -npp:
        Exclude installation of the 'pypandoc' dependency.
    --no-jedi:
        Exclude 'Jedi' support.
    --qti-demo, -qd:
        Install R/exams demo files for 'qti'.

  Example Usage:
	  %run init_rexams --rpy2ver 3.0.1 --demo-path /path/to/demo/files

R/exams is a powerful tool for  creating exams in R.
For more details and usage instructions, please refer to the script's
repository and the R/exams documentation.
  * [RExamsUtils](https://github.com/Mr-McGL/RExamsUtils)
  * [R/exams](https://www.r-exams.org/)

ToDo:
  * Improve exception management
  * Add functions into and from nbutils (such as fprnt)
  * Introduce dependencies

Additional Info:
  @Author: Marcos García-Lorenzo
  @Maintainer:Marcos García-Lorenzo
  @e-mail: marcos.garcia@urjc.es

  @Version: 0.1.0
  @Date Created: October 19th, 2023
  @Date Modified: December 5, 2023
  @Status: 2 - Pre-Alpha

  @Copyright: © 2023 by Marcos García-Lorenzo (VGLAB - MIMIC - URJC). All rights reserved.
  @License: MIT License
"""
# @Links: {'MIMIC': 'https://gestion2.urjc.es/pdi/grupos-innovacion/mimic', 'VG-LAB': 'https://vg-lab.es/', 'URJC': 'https://www.urjc.es', 'R/exams': 'https://www.r-exams.org/', 'Project-URL': 'https://github.com/Mr-McGL/RExamsUtils'}

__metadata__ = dict(
		__name__ = "init_rexams",
		__project_name__ = "RExamsUtils",
		__keywords__ = ['Jupyter', 'R', 'rpy2', 'Google Colab', 'R/exams'],
		__description__ = "This script installs the R/exams package and its dependencies for use in Jupyter Notebooks via 'rpy2'.",
		__version__ = "0.1.0",
		__date_created__ = "October 19th, 2023",
		__date_modified__ = "December 5, 2023",
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

import os

from IPython import get_ipython
import subprocess

from importlib.metadata import version as pkg_version
from packaging.version import parse as get_version
from importlib.util import find_spec

import argparse

#Auxiliar functions

#---

def reboot():
  """Reboot the Jupyter notebook kernel.

  This function restarts the Jupyter notebook kernel, clearing all previous
  variables and states. It is equivalent to restarting the notebook.

  Usage:
      reboot()
  """
  print("\n\x1B[1m\x1B[4m\x1b[35mReboot needed.\x1b[0m")
  print("\x1B[1m\x1B[4m\x1b[31mPlease rerun the notebook from the beginning.\x1b[0m")
  #%reset -f
  quit()

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

def run_R(cmd: str, line: str = '', run_cell: bool =True):
  """Run an R command in the Jupyter notebook.

  Parameters:
      cmd (str): The R command to be executed.
      line (str, optional): If provided, the command is run as a line with the specified
          line magic. Default is an empty string.
      run_cell (bool, optional): If True, the command is run as a cell magic. If False, it
          is run as a line magic. Default is True.

  Returns:
      If run_cell is True, returns None.
      If run_cell is False, returns the output of the R command.

  Usage:
    run_R("library(ggplot2)", run_cell=True)
  """
  if run_cell:
    get_ipython().run_cell_magic('R', line, cmd)
  else:
    return get_ipython().run_line_magic('R', cmd)

#---

def cell_magic(magic: str, line: str = '', cell: str = ''):
  """
  Run a cell magic command in the Jupyter notebook.

  Parameters:
      magic (str): The name of the cell magic to be executed.
      line (str, optional): The line magic command to be passed to the cell magic.
          Default is an empty string.
      cell (str, optional): The content of the cell to be executed with the cell magic.
          Default is an empty string.

  Usage:
      cell_magic("%%html", line="bgcolor='lightblue'", cell="<h1>Hello, Jupyter!</h1>")
  """
  get_ipython().run_cell_magic(magic, line, cell)

#---

def line_magic(magic: str, line: str = ''):
  """
  Run a line magic command in the Jupyter notebook.

  Parameters:
      magic (str): The name of the line magic to be executed.
      line (str, optional): The line magic command to be executed.

  Usage:
      cell_line("%matplotlib inline")
  """
  get_ipython().run_line_magic(magic, line)

#--

def warn_error_print(msg: str) -> None:
    """
    Print warning/error messages with a formatted prefix.

    This function prints the provided message with a distinctive prefix indicating. 
    The message can include newline characters for multiline output.

    Parameters:
        - msg (str): The message to be printed.

    Example:
        warn_error_print("This is a warning.")
        >> [R]: This is a warning.

    Note:
        The formatting includes color-coding and styling for clear identification of warnings/errors.
    """
    if not msg:
        return

    def print_line(m: str, add_prefix: bool, end: str = "\n"):
        prefix = "\x1b[1m\x1b[32m[R]: \x1b[0m" if add_prefix else ""
        print(f"{prefix}\x1b[3m\x1B[1m\x1b[35m{m}\x1b[0m", end=end)

    lines = msg.split('\n')
    add_prefix = warn_error_print.new_line
    for line in lines[:-1]:
        print_line(line, add_prefix)
        add_prefix = True

    if lines[-1]:
        print_line(lines[-1], add_prefix, end='')

    warn_error_print.new_line = lines[-1] == ''


# Install rpy2 + versión check
def install_rpy2(rpy2ver: str | None = None):

  print(f"\x1B[1m\x1B[4m\x1b[34mrpy2 check\x1b[0m")

  rpy2found = find_spec("rpy2") is not None

  if rpy2found and rpy2ver is not None:
    if get_version(pkg_version("rpy2")) != get_version(rpy2ver):
      print(f"\x1B[1m\x1b[32mInstalling the selected version: {rpy2ver}.\x1b[0m")
      run(f"pip install rpy2=={rpy2ver}")
      reboot()
      return False

    else:
      print(f"\x1B[1m\x1b[32mThe selected version is already installed: {rpy2ver}.\x1b[0m")

  elif rpy2found:
    if get_version(pkg_version("rpy2")) > get_version("3.5.1"):
      print("\x1B[1m\x1b[31mTo avoid any potential issues with newer versions,\nrpy2 will be downgraded to version 3.5.1 (rpy2=={pkg_version('rpy2')})\x1b[0m")
      run(f"(pip install rpy2==3.5.1)")
      reboot()
      return False

    else:
      print(f"\x1B[1m\x1b[32mThe current version of the rpy2 package is correct (rpy2=={pkg_version('rpy2')}).\x1b[0m")

  print(f"\x1B[1m\x1B[4m\x1b[34m\nLoading rpy2 extension\x1b[0m")
  reload_ext("rpy2.ipython")


# Install R/examas
def install_rexams(demo_path: str | None = None, rdev:bool = False,
                   nops_support: bool = True, pypandoc: bool = True,
                   jedi: bool = True, qti_demo = False):

  import rpy2 #Cannot guarantee it is installed up to this point.
  rpy2.rinterface_lib.callbacks.consolewrite_warnerror = warn_error_print

  warn_error_print.new_line = True
  consolewrite_warnerror_default = rpy2.rinterface_lib.callbacks.consolewrite_warnerror
  
  try:
    print(f"\x1B[1m\x1B[4m\x1b[34m\nInstalling R/exams\x1b[0m", flush=True)
    if not rdev:
      run_R('install.packages("exams", dependencies = TRUE)')
    else:
      run_R('install.packages("exams", repos = "https://R-Forge.R-project.org")')

    print(f"\x1B[1m\x1B[4m\x1b[34m\nInstalling TinyTeX for supporting PDF files\x1b[0m")
    run_R('tinytex::install_tinytex()')

    if nops_support:
      print(f"\x1B[1m\x1B[4m\x1b[34m\nInstalling packages for NOPS support.\x1b[0m")
      run("apt-get install pdftk imagemagick")

    if pypandoc:
      print(f"\x1B[1m\x1B[4m\x1b[34m\nInstalling PyPandoc.\x1b[0m")
      run("pip install pandoc -U")

    if jedi:
      print(f"\x1B[1m\x1B[4m\x1b[34m\nInstalling JEDI.\x1b[0m")
      run("pip install jedi")

    print(f"\x1B[1m\x1B[4m\x1b[34m\nImporting exams into the R environment.\x1b[0m")
    run_R('library("exams")')

    if demo_path is not None:
      if not os.path.exists(demo_path):
        os.makedirs(demo_path)

      print(f"\x1B[1m\x1B[4m\x1b[34m\nInstalling demo files at: '{demo_path}'.\x1b[0m")
      writers = '"exams2html", "exams2pdf", "exams2moodle"'
      if nops_support: writers += ', "exams2nops"'
      if qti_demo: writers += ', "exams2qti12", "exams2qti21"'

      run_R(f'exams_skeleton(dir = "{demo_path}", markup = "markdown", writer = c({writers}));')

  finally:
    rpy2.rinterface_lib.callbacks.consolewrite_warnerror = consolewrite_warnerror_default
    

if __name__ == '__main__':

  ap = argparse.ArgumentParser(description="Install the R/exmas package for use with the 'rpy2'.")

  ap.add_argument('--rpy2ver', '-rv',dest='rpy2ver', type=str, default=None,
                  help="rpy2 version to use.")
  ap.add_argument('--demo-path', '-dp',dest='demo_path', type=str, default=None,
                  help="Installation path for R/exams demo files.")
  ap.add_argument('--rdev', '-rd', dest='rdev', action='store_true',
                  help="Install the development version of R/exams. Not recomended.")
  ap.add_argument('--no-nops-support', '-nns', dest='nops_support', action='store_false',
                  help="Exclude support for NOPS.")
  ap.add_argument('--no-pypandoc', '-npp', dest='pypandoc', action='store_false',
                  help="Exclude installation of the 'pypandoc' dependency")
  ap.add_argument('--no-jedi', dest='jedi', action='store_false',
                  help="Exclude 'Jedi' support")
  ap.add_argument('--qti-demo', '-qd', dest='qti_demo', action='store_true',
                  help="Install R/exmas demo files for 'qti'")
  ap.set_defaults(rdev= False, nops_support=True, pypandoc=True,
                  jedi=True, qti_demo = False)

  args = ap.parse_args()

  install_rpy2(args.rpy2ver)
  install_rexams(args.demo_path, args.rdev, args.nops_support, args.pypandoc,
                 args.jedi,args.qti_demo)

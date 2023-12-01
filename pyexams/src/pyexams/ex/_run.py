#########################################################
# This implementation work in jupyter and regular python 
# but:
#   * in regular python you might use:  stdout=sys.stdout
#   * in Ipython you can use
#     * l=get_ipython().getoutput(cmd)
#     * get_ipython().system(cmd)
#########################################################

from IPython import get_ipython as __ip_get_ipython
import subprocess as __subprocess

def run (cmd: str, olst: bool = False, raise_on_error: bool = False):
  """Run a shell command in the Jupyter notebook.

  This function allows you to run a shell command in the Jupyter notebook. You
  can capture the command's output, print it, and raise an error if the command
  returns a non-zero exit code.

  Parameters:
      cmd (str): The shell command to be executed.
      olst (bool, optional): If True, capture the command's output as a list of lines.
          If False, print the output to the notebook. Default is False.
      raise_on_error (bool, optional): If True, raise an error if the command returns
          a non-zero exit code. If False, do not raise an error. Default is False.

  Returns:
      If olst is True, returns a list of lines from the command's output.
      If olst is False, returns None.

  Raises:
      OSError: If raise_on_error is True and the command returns a non-zero exit code.

  Usage:
      run("ls -l", olst=True, raise_on_error=True)
  """
  if raise_on_error:
    proc = __subprocess.run(cmd, shell=True, stdout=__subprocess.PIPE, stderr=__subprocess.STDOUT, text=True)

    if not olst: print(proc.stdout)
    if proc.returncode !=0: raise OSError(proc)

    if olst:  return proc.stdout
    else: return

  #Ipython code for !
  elif olst:
    return __ip_get_ipython().getoutput(cmd)

  #Ipython code for !
  else:
    __ip_get_ipython().system(cmd)

#Simpler version
#def run(cmd, lst = False):
#  if lst: return get_ipython().getoutput(cmd)
#  else: get_ipython().system(cmd)


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
      cell_magic("html", line="bgcolor='lightblue'", cell="<h1>Hello, Jupyter!</h1>")
  """
  __ip_get_ipython().run_cell_magic(magic, line, cell)

#---

def line_magic(magic: str, line: str = ''):
  """
  Run a line magic command in the Jupyter notebook.

  Parameters:
      magic (str): The name of the line magic to be executed.
      line (str, optional): The line magic command to be executed.

  Usage:
      line_magic("matplotlib", "inline")
  """
  __ip_get_ipython().run_line_magic(magic, line)
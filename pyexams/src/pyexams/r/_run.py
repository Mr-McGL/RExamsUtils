from IPython import get_ipython as __get_ipython

def run(cmd: str, line: str = '', run_cell: bool =True):
  """Run an R command in the Jupyter notebook.

  Parameters:
      cmd (str): The R command to be executed.
      line (str, optional): Cell magic parameters. Default is an empty string.
      run_cell (bool, optional): If True, the command is run as a cell magic. If False, it
          is run as a line magic. Default is True.

  Returns:
      If run_cell is True, returns None.
      If run_cell is False, returns the output of the R command.

  Usage:
    run_R("library(ggplot2)", run_cell=True)
  """
  if run_cell:
    __get_ipython().run_cell_magic('R', line, cmd)
  else:
    return __get_ipython().run_line_magic('R', cmd)
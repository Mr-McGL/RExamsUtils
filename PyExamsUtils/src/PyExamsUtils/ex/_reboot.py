
from ..fprnt import fprnt as __fp_fprnt
#from IPython import get_ipython as __ipy_get_ipython

def reboot():
  """Reboot the Jupyter notebook kernel.

  This function restarts the Jupyter notebook kernel, clearing all previous
  variables and states. It is equivalent to restarting the notebook.

  Usage:
      reboot()
  """
  __fp_fprnt("Reboot needed.", frmt="bu", fg="m")
  __fp_fprnt("Please rerun the notebook from the beginning.", frmt="bu", fg="m")
  #__ipy_get_ipython().run_line_magic("reset", "-f")
  quit()

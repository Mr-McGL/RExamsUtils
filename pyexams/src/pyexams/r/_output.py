from ..fprnt import setFormat as _sf
from ..types import static_vars as _sv

from typing import Literal
import rpy2

################################################################################

def _print_line(msg: str,
              promt: str = '',
              add_promt: bool = True,
              promt_format: str = '',
              msg_format: str = '',
              end: str = '\n'):
  """
  Print a formatted line with an optional prompt.

  Parameters:
      - msg (str): The message to be printed.
      - promt (str, optional): The prompt to be displayed before the message. Default is an empty string.
      - add_promt (bool, optional): Whether to include the prompt or not. Default is True.
      - promt_format (str, optional): Formatting for the prompt. Default is an empty string.
      - msg_format (str, optional): Formatting for the message. Default is an empty string.
      - end (str, optional): The string to append at the end. Default is a newline.
  """
  prefix = f"{promt_format}{promt}{_sf('r')}" if add_promt else ''
  print (f"{prefix}{msg_format}{msg}{_sf('r')}", end = end)

################################################################################

def _print_lines(msg: str,
                new_line: bool,
                promt: str,
                promt_format: str,
                msg_format: str):
  """
  Print formatted lines with an optional prompt.

  Parameters:
      - msg (str): The message to be printed.
      - new_line (bool): Whether to start a new line before printing.
      - promt (str): The prompt to be displayed.
      - promt_format (str): Formatting for the prompt.
      - msg_format (str): Formatting for the message.

  Returns:
      bool: True if the last line is empty, False otherwise.
  """

  def _pl (msg, add_promt = True, end='\n'):
    _print_line(msg, promt, add_promt, promt_format, msg_format, end)

  lines = msg.split('\n')
  add_promt = new_line
  for line in lines[:-1]:
    _pl(line, add_promt)
    add_promt = True

  if lines[-1]:
    _pl(lines[-1], add_promt, end='')

  return lines[-1] == ''

################################################################################

def _get_param(val:str | Literal['default'], default:str): #Todo: No me gusta el literal default
  if val == 'default': return default
  else: return val

################################################################################

@_sv(__new_line = True,
             promt = '',
             promt_format = '',
             msg_format   = '')
def _pconsole(msg: str) -> None:
  """
  Print formatted lines using pconsole's static variables to define a prompt,
  prompt format, and message format.

  Parameters:
      - msg (str): The message to be printed.
  """
  if not msg: return

  _pconsole.__new_line = _print_lines(msg, _pconsole.__new_line, _pconsole.promt,
                                   _pconsole.promt_format, _pconsole.msg_format)

################################################################################

@_sv(__new_line = True,
             promt = "[R] > ",
             promt_format = _sf ('bi', ('fg', 200, 100 , 0)),
             msg_format   = _sf ('bi', ('fg', 223, 165 , 0)))
def _pwarnerr(msg: str) -> None:
  """
  Print warning/error messages using pwarnerr's static variables to define a prompt,
  prompt format, and message format.

  Parameters:
      - msg (str): The message to be printed.
  """


  if not msg: return

  _pwarnerr.__new_line = _print_lines(msg, _pwarnerr.__new_line, _pwarnerr.promt,
              _pwarnerr.promt_format, _pwarnerr.msg_format)

################################################################################

@_sv(_default_func = rpy2.rinterface_lib.callbacks.consolewrite_print)
def set_console_cb(default: bool = False,
                   promt:        None | str | Literal['default'] = None,
                   promt_format: None | str | Literal['default'] = None,
                   msg_format:   None | str | Literal['default'] = None) -> None:
  """
  Set the console callback function for printing in R.

  Customize the printing behavior by configuring the prompt, prompt format,
  and message format using this function. Utilize pyexams.fprnt.setFormat to
  define both prompt and message formats.

  Parameters:
      - default (bool, optional): Restore the default R's printing behavior. If True, other parameters are ignored. Default is False.
      - prompt (None | str | Literal['default'], optional): Set the prompt style. Default is None, retaining the previous one.
      - prompt_format (None | str | Literal['default'], optional): Set the prompt format. Default is None, retaining the previous one.
      - msg_format (None | str | Literal['default'], optional): Set the message format. Default is None, retaining the previous one.
  """
  if default:
    rpy2.rinterface_lib.callbacks.consolewrite_print = set_console_cb._default_func
    return

  if promt is not None:
    _pconsole.promt = _get_param(promt, '')

  if promt_format is not None:
    _pconsole.promt_format = _get_param(promt_format, '')

  if msg_format is not None:
    _pconsole.msg_format = _get_param(msg_format, '')

  rpy2.rinterface_lib.callbacks.consolewrite_print = _pconsole
################################################################################

@_sv(_default_func = rpy2.rinterface_lib.callbacks.consolewrite_warnerror)
def set_warnerr_cb(default: bool = False,
                   promt:        None | str | Literal['default'] = None,
                   promt_format: None | str | Literal['default'] = None,
                   msg_format:   None | str | Literal['default'] = None) -> None:
  """
  Set the console callback function for warning/error messages in R.

  Customize the behavior of warning/error messages by configuring the prompt,
  prompt format, and message format using this function. Utilize pyexams.fprnt.setFormat
  to define both prompt and message formats.

  Parameters:
      - default (bool, optional): Restore the default callback function. If True, other parameters are ignored. Default is False.
      - prompt (None | str | Literal['default'], optional): Set the prompt style. Default is None, retaining the previous one.
      - prompt_format (None | str | Literal['default'], optional): Set the prompt format. Default is None, retaining the previous one.
      - msg_format (None | str | Literal['default'], optional): Set the message format. Default is None, retaining the previous one.
  """
  if default:
    rpy2.rinterface_lib.callbacks.consolewrite_warnerror = set_warnerr_cb._default_func
    return

  if promt is not None:
    _pwarnerr.promt = _get_param(promt, "[R] > ")

  if promt_format is not None:
    _pwarnerr.promt_format = _get_param(promt_format, _sf('bi', ('fg', 200, 100 , 0)))

  if msg_format is not None:
    _pwarnerr.msg_format = _get_param(msg_format, _sf('bi', ('fg', 223, 165 , 0)))

  rpy2.rinterface_lib.callbacks.consolewrite_warnerror = _pwarnerr


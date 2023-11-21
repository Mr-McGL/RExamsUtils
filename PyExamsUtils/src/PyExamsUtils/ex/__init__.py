# -*- coding: utf-8 -*-
''' Excution utils

TODO:
  * remove _ and use the modules!!!!
'''

from ._run import run, cell_magic, line_magic
from ._envcheck import runningInColab, runningInRemoteColab, runningInLocalColab, isColabToolkitInstalled
from ._path import find_in_paths, sys_paths, add2syspath
from ._reboot import reboot

from ._basics import __param, __r_mat, __c_n, __build_dict
from ..fprnt import fprnt
from ..r import run

from typing import Literal, Sequence, cast
import random


def __render(
  renderer: Literal["html","pandoc","moodle","pdf","nops"],

  exercise_templates: str | Sequence[str | Sequence[str]],
  
  return_metadata:    bool                                     = True,
  
  verbose:            Literal["quiet","low","moderate","all"]  = "quiet",

  n:                  int                                      = 1,
  gseed:              int | None                               = None,
  seed:               int | Sequence[Sequence[int]] | None     = None,
  
  **kwargs) -> None | dict: 
  #Todo: Warning - check: param("name", name) --- Encoding(name) <- "UTF-8"
  
  # PARAMETERS
  ############
  __param.reset()
  params = __param('', exercise_templates)
  params += __param('n', n)

  for k, v in kwargs.items():
    params += __param(k, v)

  #verbose
  if verbose == "moderate" or verbose == "all":
    params += __param("verbose", True)
    if verbose == "all":
      params += __param("quiet", False)

  #Local seeds
  seed_mat : list[list[int]] = [[]]
  #if seed is None: seed_mat = __r_mat(n, n_ets)
  if seed is not None:
    n_ets = 1 if isinstance(exercise_templates, str) else sum(1 if isinstance(et, str) else len(et) for et in exercise_templates)
    seed_mat = __r_mat(n, n_ets, seed) if isinstance(seed, int) else list(map(list, cast(Sequence[Sequence[int]], seed)))
    params += f"{__param.np}seed = matrix({__c_n([e for row in seed_mat for e in row])}, nrow = {n}, ncol = {n_ets}, byrow = TRUE)"

  # CODE
  ######

  code = ""

  #Seed (Global)
  gs: int = 0
  if seed is None: #2147483647 - max int 32bits
    gs = random.randint(1, 2147483640) if gseed is None else gseed
    code += f"set.seed({gs})\n"

  code +=  f"exam = exams2{renderer}({params})\n"

  if return_metadata or verbose in ("low", "moderate", "all"):
    code += "md = exams_metainfo(exam)\n"

  if verbose in ("low", "moderate", "all"):
    code += "print(md)\n"
    fprnt(code, fg = 34)
   
  run(code)

  # Return metadata
  #################
  if return_metadata:
    md = __build_dict(run("md", run_cell = False))
    return {'exams': md,
            'seeds': {
                      'type': 'global' if seed is None else 'local',
                      'val':  gs if seed is None else seed_mat
                     }
            }
  
  return None # ToDo, no debería ser necesario


from typing import Sequence
from ..types import is_seq, is_seq_of_seq_or_bt, static_vars


import random

import sys
import os

from rpy2.robjects.vectors import ListVector as rpy2LV
from rpy2.rinterface_lib.sexp import NULLType as rpy2Null

class __RawParam(str):
  """
  This class is allows to include parameters supported by R/Exmas renderers that have 
  not yet been included in this Python wrapper.
  """
  def __new__(cls, value): return super().__new__(cls, value)

def __bool(val: bool) -> str: return 'TRUE' if val else 'FALSE'
def __str (val: str)  -> str: return f'"{val}"'

def __c_s(seq: Sequence[str], func: str = 'c') -> str:
  return  f'{func}({", ".join(map(__str , seq))})'

def __c_b(seq: Sequence[bool], func: str = 'c') -> str:
  return f'{func}({", ".join(map(__bool, seq))})'

def __c_n(seq: Sequence[int | float | complex], func: str = 'c') -> str:
  return f'{func}({", ".join(map(str, seq))})'

def __c(seq: Sequence, func: str = 'c') -> str:
  def toStr(item) -> str:
    if isinstance(item, bool): return __bool(item)
    elif isinstance(item, str): return __str(item)
    elif isinstance(item,(int, float, complex)): return str(item)
    else: raise ValueError(f"Invalid type: {type(item)}")

  return f'{func}({", ".join(map(toStr, seq))})'

def __c_seq(seq: Sequence, func: Sequence[str] | None = None) -> str:
  f = func if func is not None else ("list", "c")
  def toStrS(item) -> str:
    if isinstance(item, bool): return __bool(item)
    elif isinstance(item, str): return __str(item)
    elif isinstance(item, (int, float, complex)): return str(item)
    elif isinstance(item, Sequence): return __c(item, f[-1])
    else: raise ValueError(f"Invalid type: {type(item)}")

  return f'{f[0]}({", ".join(map(toStrS, seq))})'


def __create_dir(dir:str|None):
  if dir: os.makedirs(dir, exist_ok=True)


def __reset(): __param.np = '\n\t'

@static_vars(np = ',\n\t',
             reset = __reset)
def __param(var: str, val) -> str:
  if val is None: return ''
  elif isinstance(val, __RawParam): rval = str(val)
  elif isinstance(val, str): rval = f'"{val}"'
  elif isinstance(val, bool):   rval = __bool(val)
  elif isinstance(val, (int, float, complex)): rval = str(val)
  elif isinstance(val, Sequence):
    if is_seq(val,str): rval = __c_s(val)
    elif is_seq(val,bool): rval = __c_b(val)
    elif is_seq(val, (int, float, complex)): rval = __c_n(val)
    elif is_seq_of_seq_or_bt(val, str) or \
         is_seq_of_seq_or_bt(val, bool) or \
         is_seq_of_seq_or_bt(val, (int, float, complex)):
      rval = __c_seq(val)
    else: raise ValueError(f"Invalid type: {type(val)}")
  elif isinstance(val, dict):
    np_old,__param.np = __param.np, f"{__param.np.replace(',','',1)}\t"
    rval = f'list({"".join(__param(k,v) for k, v in val.items())})'
    __param.np = np_old   
  else: raise ValueError(f"Invalid type: {type(val)}")

  param = f'{__param.np}{var} = {rval}' if var !='' else f'{__param.np}{rval}'
  if __param.np[0] != ',': __param.np = f',{__param.np}' # Adds ',' after first param

  return param


def __build_dict(listVec):
  def map_func(item):
    if isinstance(item, rpy2LV): return __build_dict(item)
    elif isinstance(item, rpy2Null): return ''
    else:
      li = list(item)
      if len(li) == 0: return ''
      elif len(li) == 1: return li[0]
      return li

  if isinstance(listVec.names, rpy2Null):
    return {f'{i}': map_func(e) for i, e in enumerate(list(listVec))}
  else:
    return dict(zip(listVec.names, map(map_func, list(listVec))))

def __r_mat(r: int, c: int, s: int | None = None) -> list[list[int]]:
  if s is not None:  random.seed(s)
  return [[random.randint(1, 2147483640) for _ in range(c)] for _ in range(r)] #2147483647 - max int 32bits
  # str(float(str(r)))==str(r)?????
  #return [[random.random() for _ in range(c)] for _ in range(r)]


def print_metadata(meta_data: dict) -> None:
  """
  Print metadata information from a dictionary containing exercise data.

  Parameters:
      meta_data (dict): A dictionary containing metadata information for exercises.

  Prints:
      None

  The function iterates over the items in the input dictionary, assuming it has a structure where the keys represent exams and the values are dictionaries containing information about exercises. For each exam, it prints the exam name and then iterates over the exercises within that exam, printing the exercise number, name, and associated string information.

  Example:
  --------
  meta_data = {
      'exam1': {
          'exercise1': {'string': 'Swiss Capital: b'}, # ... (other values)
          'exercise2': {'string': 'Analysis of variance: a, c, d'}, # ... (other values)
          # ... (other exercises)
      },
      'exam2': {
          'exercise1': {'string': 'Swiss Capital: c'}, # ... (other values)
          'exercise2': {'string': 'Analysis of variance: c, d'}, # ... (other values)
          # ... (other exercises)
      },
      # ... (other exams)
  }

  Usage:
  ------
  print_metadata(meta_data)
  """
  for exam, exercises in meta_data["exams"].items():
    print(f'{exam}:')
    for i, (name, exercise) in enumerate(exercises.items()):
      print(f"    {i+1}. {exercise['string']}")

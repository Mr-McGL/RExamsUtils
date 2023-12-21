from ._basics import __str, __c_s
from ..r import run

from typing import Literal, Sequence
import os

__markups = ("markdown","latex")
__writers = ("exams2html", "exams2pdf", "exams2moodle", "exams2qti12", "exams2qti21", "exams2arsnova", "exams2nops")
__question_types = ("num", "schoice", "mchoice", "string", "cloze")

__markupsLiterals = Literal["markdown","latex"]
__writeLiterals = Literal["exams2html", "exams2pdf", "exams2moodle", "exams2qti12", "exams2qti21", "exams2arsnova", "exams2nops"]
__question_typeLiterals = Literal["num", "schoice", "mchoice", "string", "cloze"]

__writerT = None | Sequence[__writeLiterals] | __writeLiterals | Literal["all"]
__question_typeT = None | Sequence[__question_typeLiterals] | __question_typeLiterals | Literal["all"]

def skeleton(dir: str = "exams",
             markup:          __markupsLiterals = "markdown",
             addmarkup2path:  bool              = True,
             writer :         __writerT         = None,
             question_type:   __question_typeT  = None) -> None:
  """
    Generate a directory structure which contains demo scripts, exsercice templates, and written and XML exam templates.

    Parameters:
        dir (str, optional): The directory where the R/exams files will be stored. Default is "exams".
        markup (str, optional): The markup language to be used, either "markdown" or "latex". Default is "markdown".
        addmarkup2path (bool, optional): Whether to include the markup language in the directory path. Default is True.
        writer (None, str, Sequence[str], Literal["all"], optional): The R/exam writer(s) to be used.
            It can be a single writer (string), a list of writers, "all" for all writers, or None for default writers.
            Default is None.
        question_type (None, str, Sequence[str], Literal["all"], optional): The type(s) of questions to include.
            It can be a single question type (string), a list of question types, "all" for all types, or None for all types.
            Default is None.

    Returns:
        None: The function generates the exams skeleton but does not return a value.

    Example:
        skeleton(dir="myexams", markup="latex", addmarkup2path=False, writer="exams2pdf", question_type="num")
    """

  dirStr = f"{dir}/{markup}" if addmarkup2path else dir
  os.makedirs(dirStr, exist_ok=True)

  if writer is None:
    writerStr = 'c("exams2html", "exams2pdf", "exams2moodle")'
  elif isinstance(writer, str) and writer != "all":
    writerStr = __str(writer)
  elif writer == "all" or isinstance(writer,Sequence):
    writerStr = __c_s(__writers if writer == 'all' else writer)

  if question_type is None:
    typeStr = ""
  elif isinstance(question_type, str) and question_type != "all":
    typeStr = f',\n        type={__str(question_type)}'
  elif question_type == "all" or isinstance(question_type, Sequence):
    typeStr = f',\n        type={__c_s(__question_types if question_type == "all" else question_type)}'


  run(f"""
    exams_skeleton(
        dir = "{dirStr}",
        markup = "{markup}",
        encoding = "UTF-8",
        writer = {writerStr} {typeStr})
  """)
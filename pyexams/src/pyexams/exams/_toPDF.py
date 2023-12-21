from ._render import __render
from ._basics import __create_dir, __RawParam

from typing import Literal, Sequence


def toPDF(
  exercise_templates: str | Sequence[str | Sequence[str]],

  return_metadata:    bool                                     = True,
  verbose:            Literal["quiet","low","moderate","all"]  = "quiet",

  name:               str | None                               = None,

  n:                  int                                      = 1,
  nsamp:              int | Sequence[int] | None               = None,

  gseed:              int | None                               = None,
  seed:               int | Sequence[Sequence[int]] | None     = None,
  
  exshuffle:          bool | int | None                        = None,
  points:             int | Sequence[int|Sequence[int]] | None = None,

  template:           str | None                               = None,
  inputs:             str | Sequence[str] | None               = None,
  header:             dict | None                              = None, 
  texengine:          str | None                               = None,
  attachfile:         bool | None                              = None,

  odir:               str                                      = '.',
  edir:               str | None                               = None,
  tdir:               str | None                               = None,
  sdir:               str | None                               = None,
  texdir:             str | None                               = None,

  rds:                bool | None                              = None,

  **kwargs) -> None | dict: 
  """
  Convert R/exams exercise templates to PDF format.

  Parameters:
    exercise_templates (str or Sequence[str or Sequence[str]]): Path(s) of the R/exams exercise template file(s).

    return_metadata (bool, optional): Specify whether to return metadata information. Default is True.
    verbose (Literal["quiet","low","moderate","all"], optional): Level of verbosity during the conversion process.
        Options: "quiet", "low", "moderate", or "all". Default is "quiet".

    name (str or None, optional): Prefix to be added to the resulting exams. Default is None.

    n (int, optional): Number of copies to compile from the exercise template. Default is 1.
    nsamp (int or Sequence[int] or None, optional): Number(s) of exercise files sampled from each template.
      Sampling without replacement is used if possible. Default is None.

    gseed (int or None, optional): Set a global seed for the entire exam. If set to None and seed is None,
        the global seed will be generated randomly. Default is None.
    seed (int or Sequence[Sequence[int]] or None, optional): Set local seeds for each question.
        If not None, it overrides gseed. Not recommended for `nsamp` greater than 1. Default is None.

    exshuffle (bool or int or None, optional): Overrides the exshuffle tag from the file.
        For example, exshuffle = False can be used to keep all available answers without permutation. Default is None.
    points (int or Sequence[int or Sequence[int]] or None, optional): Specify how many points should be assigned to each exercise.
        Note that this argument overrides any exercise points that are provided within the expoints tags of the exercise files (if any).
        The vector of points supplied should either have length 1 or the number of exercises in the exam. Default is None.

    template (str or None, optional): Specify the LaTeX template.
        The package currently provides "plain.tex". Default is None.
    inputs (str or Sequence[str] or None, optional): Names of files that are needed as inputs during LaTeX compilation (e.g., style files, headers).
        Either the full path must be given or the file needs to be in edir. Default is None.
    header (dict or None, optional): A list of further options to be passed to the LaTeX files. Default is None.
    texengine (str or None, optional): Passed to latexmk if tinytex is available. Default is None.
    attachfile (bool or None, optional): Specify whether the LaTeX commands url and href should be replaced by attachfile commands when used for supplementary files.
        This enables embedding these supplementary files directly into the PDF when the template loads the attachfile LaTeX package. Default is None.

    odir (str or None, optional): Output directory. Default is '.'.
    edir (str or None, optional): Path of the directory where exercise templates are stored. Default is None.
    tdir (str or None, optional): Temporary directory. Default is None.
    sdir (str or None, optional): Directory for storing supplements. Default is None.
    texdir (str or None, optional): Directory for running texi2dvi in. Default is None.

    rds (bool or None, optional): Specify whether the return list should also be saved as an RDS (R Data Serialization) file. 
        Default is None.

    **kwargs (optional): Additional parameters. See `exams2pdf` (R/exams' documentation) for more details. *Strings must be quoted*. 

  Returns:
    None or dict: If return_metadata is True, returns metadata information. Otherwise, returns None.
  """

  __create_dir(odir) 
  __create_dir(tdir)
  __create_dir(sdir)
  __create_dir(texdir)

  pkwargs = {k: __RawParam(v) for k, v in kwargs.items()}
    
  return __render("pdf", exercise_templates,
      return_metadata = return_metadata, verbose = verbose, 
      name = name, 
      n = n, nsamp = nsamp, gseed = gseed, seed = seed, 
      exshuffle = exshuffle, points = points, 
      template = template, inputs = inputs, header = header, 
      texengine = texengine, attachfile = attachfile, 
      dir = odir, edir = edir, tdir = tdir, sdir = sdir, texdir = texdir, 
      rds = rds, 
      **pkwargs)

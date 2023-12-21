from ._render import __render
from ._basics import __create_dir, __RawParam

from typing import Literal, Sequence



def toHTML(
  exercise_templates: str | Sequence[str | Sequence[str]],

  return_metadata:    bool                                     = True,
  verbose:            Literal["quiet","low","moderate","all"]  = "quiet",

  name:               str | None                               = None,

  n:                  int                                      = 1,
  nsamp:              int | Sequence[int] | None               = None,

  gseed:              int | None                               = None,
  seed:               int | Sequence[Sequence[int]] | None     = None,
  
  exshuffle:          bool | int | None                        = None,
  question:           bool | str | None                        = None,
  solution:           bool | str | None                        = None,

  template:           str | None                               = None,
  svg:                bool | None                              = None,
  mathjax:            bool | None                              = None,
  base64:             bool | str | Sequence[str] | None        = None, #["png"]

  resolution:         int | None                               = None,
  width:              int | None                               = None,
  height:             int | None                               = None,

  odir:               str                                      = '.',
  edir:               str | None                               = None,
  tdir:               str | None                               = None,
  sdir:               str | None                               = None,

  rds:                bool | None                              = None,

  **kwargs) -> None | dict: 
  """
  Converts R/exams exercise templates to HTML format.

  Parameters:
    exercise_templates (str or Sequence[str or Sequence[str]]): Path(s) of the R/exams exercise template file(s).

    return_metadata (bool, optional): Specify whether to return metadata information. Default is True.
    verbose (Literal["quiet", "low", "moderate", "all"], optional): Level of verbosity during the conversion process.
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
    question (bool or str or None, optional): Specify whether the question should be included in the HTML output.
        If a string, it will be used as a header for resulting questions. Default is None.
    solution (bool or str or None, optional): Specify whether the solution should be included in the HTML output.
        If a string, it will be used as a header for resulting solutions. Default is None.

    template (str or None, optional): Specify the HTML template.
        The package currently provides "plain.html". Default is None.
    svg (bool, optional): Specify whether the SVG graphics should be included in the HTML output. Default is False.
    mathjax (bool, optional): Specify whether the JavaScript from http://www.MathJax.org/ should be included for rendering mathematical formulas.
        Default is False.
    base64 (bool or str or Sequence[str] or None, optional): Specify whether images should be embedded using Base 64 coding.
        If a string, it should be a character vector of file endings that should be Base 64 encoded. Default is None.

    resolution (int or None, optional): Options for rendering PNG (or SVG) graphics passed to xweave. Default is None.
    width (int or None, optional): Width for rendering PNG (or SVG) graphics. Default is None.
    height (int or None, optional): Height for rendering PNG (or SVG) graphics. Default is None.

    odir (str or None, optional): Output directory. Default is '.'.
    edir (str or None, optional): Path of the directory where exercise templates are stored. Default is None.
    tdir (str or None, optional): Temporary directory. Default is None.
    sdir (str or None, optional): Directory for storing supplements. Default is None.

    rds (bool or None, optional): Specify whether the return list should also be saved as an RDS (R Data Serialization) file. 
        Default is None.

    **kwargs (optional): Additional parameters. See `exams2html` (R/exams' documentation) for more details. *Strings must be quoted*. 

  Returns:
    None or dict: If return_metadata is True, returns metadata information. Otherwise, returns None.
  """ # ToDo: Check: Default is vs the default value is ...
  
  #https://stackoverflow.com/questions/62536479/the-command-exams2html-does-not-generate-html-page-when-it-is-run-from-rstudio
  __create_dir(odir) 
  __create_dir(tdir)
  __create_dir(sdir)

  pkwargs = {k: __RawParam(v) for k, v in kwargs.items()}
  
  
  return __render("html", exercise_templates,
      return_metadata = return_metadata, verbose = verbose, 
      name = name, 
      n = n, nsamp = nsamp, gseed = gseed, seed = seed, 
      exshuffle = exshuffle,question = question, solution = solution, template = template, 
      svg = svg, mathjax = mathjax, base64 = base64, 
      resolution = resolution, width = width, height = height,
      dir = odir, edir = edir, tdir = tdir, sdir = sdir, #odir is dir!
      rds = rds,
      **pkwargs)

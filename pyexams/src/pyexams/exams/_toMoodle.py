from ._render import __render
from ._basics import __create_dir, __RawParam

from typing import Literal, Sequence


def toMoodle(
  exercise_templates: str | Sequence[str | Sequence[str]],

  return_metadata:    bool                                     = True,
  verbose:            Literal["quiet","low","moderate","all"]  = "quiet",

  name:               str | None                               = None,

  n:                  int                                      = 1,
  nsamp:              int | Sequence[int] | None               = None,

  gseed:              int | None                               = None,
  seed:               int | Sequence[Sequence[int]] | None     = None,
  
  shuffle:            bool | None                        = None,
  points:             int | Sequence[int|Sequence[int]] | None = None,
  eval:               dict | None                              = None,
  solution:           bool | None                              = None,

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

  table:               str | None                              = None,
  css:                 str | Sequence[str] | None              = None,  #paths or html
  iname:               bool | None                             = None,  #$course$/ExamName/
  stitle:              str | None                              = None,  #$course$/ExamName/SectionName.
  testid:              bool | None                             = None,
  zip:                 bool | None                             = None,
  num:                 dict | None                             = None,
  mchoice:             dict | None                             = None,
  schoice:             dict | None                             = None,
  string:              dict | None                             = None,
  cloze:               dict | None                             = None,
  pluginfile:          bool | None                             = None,
  forcedownload:       bool | None                             = None,
  answernumbering:     Literal["abc", "ABCD", 
                               "123", "none"] | None           = None,
  usecase:             bool | None                             = None,
  essay:               bool | None                             = None,
  numwidth:            bool | int | str | None                 = None,
  stringwidth:         bool | int | str | None                 = None,
  abstention:          bool | str | None                       = None,
  truefalse:           str | None                              = None,  # len(truefalse)==2

  rds:                bool | None                              = None,

  **kwargs) -> None | dict: 
  """
  Converts R/exams exercise templates to Moodle XML format.

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

    shuffle (bool or int or None, optional): Overrides the exshuffle tag from the file.
        For example, shuffle = False can be used to keep all available answers without permutation. Default is None.
    points (int or Sequence[int or Sequence[int]] or None, optional): Specify how many points should be assigned to each exercise.
    eval (dict or None, optional): Evaluation settings. Default is None.
    solution (bool or None, optional): Specify whether the solution should be included in the Moodle XML output. Default is None.

    svg (bool, optional): Specify whether the SVG graphics should be included in the HTML output. Default is False.
    mathjax (bool, optional): Specify whether the JavaScript from http://www.MathJax.org/ should be included for rendering mathematical formulas.
        Default is False.
    base64 (bool or str or Sequence[str] or None, optional): Specify whether images should be embedded using Base 64 coding.
    inputs (str or Sequence[str] or None, optional): Names of files that are needed as inputs during LaTeX compilation (e.g., style files, headers).
        If a string, it should be a character vector of file endings that should be Base 64 encoded. Default is None.

    resolution (int or None, optional): Options for rendering PNG (or SVG) graphics passed to xweave. Default is None.
    width (int or None, optional): Width for rendering PNG (or SVG) graphics. Default is None.
    height (int or None, optional): Height for rendering PNG (or SVG) graphics. Default is None.

    odir (str or None, optional): Output directory. Default is '.'.
    edir (str or None, optional): Path of the directory where exercise templates are stored. Default is None.
    tdir (str or None, optional): Temporary directory. Default is None.
    sdir (str or None, optional): Directory for storing supplements. Default is None.

    table (str or None, optional): An optional class assigned to <table> elements in the question. Default is None.
    css (str or Sequence[str] or None, optional): Path(s) to CSS style file(s) or HTML style string. Default is None.
    iname (bool or None, optional): Whether the exam name should be included in the path in the <category> tag in the final XML file.
        This option may be useful when questions should be added to certain already existing question banks.
        If True, the exam name will be included by $course$/ExamName/. Default is None.
    stitle (str or None, optional): For the questions specified in argument file, additional section titles may be set.
        The section titles will then be added to the <category> tag in the final XML file (see also argument iname).
        Default is None.
    testid (bool or None, optional): Specify whether a unique test id should be added to the exam name. Default is None.
    zip (bool or None, optional): Specify whether the resulting XML file should be zipped. Default is None.
    num (dict or None, optional): Options applied to numerical questions. See R/exams' documentation for more details. 
      Default is None.
    mchoice (dict or None, optional): Options applied to multiple choice questions. See R/exams' documentation for more details. 
        Default is None.
    schoice (dict or None, optional): Options applied to single choice questions. See R/exams' documentation for more details. 
        If None, schoice = mchoice. Default is None.
    string (dict or None, optional): Options applied to string questions. See R/exams' documentation for more details. 
      Default is None.
    cloze (dict or None, optional): Options applied to to cloze questions. See R/exams' documentation for more details. 
      Default is None.

    pluginfile (bool or None, optional): Specify whether supplements should be included in the Moodle XML file via Moodle’s Pluginfile mechanism.
        This is the default but may not work with older versions of Moodle (<2.5). Default is None.
    forcedownload (bool or None, optional): Specify whether all supplementary links should be forced to download when clicked
        (as opposed to opening in the browser). Only supported if pluginfile = TRUE. Default is None.
    answernumbering (Literal["abc", "ABCD", "123", "none"] or None, optional):
        Specify how choice questions should be numbered. Default is None.
    
    usecase (bool or None, optional): Specify whether string questions should be case sensitive or not. Default is None.
    essay (bool or None, optional): Specify whether string questions should be rendered into Moodle shortanswer or essay questions.
        The default is to use shortanswer unless either essay=True or the exercise’s metainformation is set to essay. Default is None.
    numwidth (bool, int, str, or None, optional): Specify whether the width of all num sub-items in a cloze should be fixed to the same width?
        Default is None.
    stringwidth (bool, int, str, or None, optional): Specify whether the width of all string sub-items in a cloze should be fixed to the same width?
        Default is None.
    abstention (bool, str, or None, optional): Specify whether an explicit abstention option should be added in single/multiple choice exercises?
        The character text specified is used for an extra button in Moodle which (when selected) always leads to zero points.
        Default is None.
    truefalse (str or None, optional): For single choice answers in cloze questions, the user may specify the possible options shown.
        Default is None.  # len(truefalse)==2

    rds (bool or None, optional): Logical indicating whether the return list should also should be saved as an RDS (R Data Serialization) file. 
      Default is None.

    **kwargs (optional): Additional parameters. See `exams2moodle` (R/exams' documentation) for more details. *Strings must be quoted*. 

  Returns:
    None or dict: If return_metadata is True, returns metadata information. Otherwise, returns None.
  """
   
  #https://stackoverflow.com/questions/62536479/the-command-exams2html-does-not-generate-html-page-when-it-is-run-from-rstudio
  __create_dir(odir) 
  __create_dir(tdir)
  __create_dir(sdir)

  pkwargs = {k: __RawParam(v) for k, v in kwargs.items()}
  
  
  return __render("moodle", exercise_templates,
      return_metadata = return_metadata, verbose = verbose, 
      name = name, 
      n = n, nsamp = nsamp, gseed = gseed, seed = seed, 
      shuffle = shuffle, #exshuffle = exshuffle,
      points = points, eval = eval, solution = solution,  
      svg = svg, mathjax = mathjax, base64 = base64, 
      resolution = resolution, width = width, height = height,
      dir = odir, edir = edir, tdir = tdir, sdir = sdir, #odir is dir!
      table = table, css = css, 
      iname = iname, stitle = stitle, testid = testid, zip = zip, 
      num = num, mchoice = mchoice, schoice = schoice, string = string, cloze = cloze, 
      pluginfile = pluginfile, forcedownload = forcedownload, 
      answernumbering = answernumbering, usecase = usecase, 
      essay = essay, numwidth = numwidth, stringwidth = stringwidth, 
      abstention = abstention, truefalse = truefalse,        
      rds = rds,
      **pkwargs)

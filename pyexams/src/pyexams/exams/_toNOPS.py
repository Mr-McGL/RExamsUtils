from ._render import __render
from ._basics import __create_dir, __RawParam

from typing import Literal, Sequence

def toNOPS(
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
  nchoice:            int | None                               = None,

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

  language:      Literal["en", "es", "nl", "fr", "de", 
                         "it", "ro", "pt", "tr"]               = "es",
  title:         str | None                                    = None,
  course:        str | None                                    = None,
  institution:   str | None                                    = None,
  logo:          str | None                                    = None,
  date:          str | None                                    = None, 
  replacement:   bool | None                                   = None,
  intro:         str | Sequence[str] | None                    = None, # File.text or vector with LaTeX
  blank:         int | None                                    = None, # blank pages
  duplex:        bool | None                                   = None,
  pages:         str | Sequence[str] | None                    = None, # paths to PDFs
  usepackage:    str | Sequence[str] | None                    = None, #Latex packages
  startid:       int | None                                    = None,
  showpoints:    bool | None                                   = None,
  samepage:      bool | None                                   = None,
  twocolumn:     bool | None                                   = None,
  reglength:     int | None                                    = None,



  rds:                bool | None                              = None,

  **kwargs) -> None | dict: 
  """
  Convert R/exams exercise templates to NOPS (Written Exams for Automatic Evaluation).

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
    nchoice (int or None, optional): Number of choice alternatives per exercise. Default is None.

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

    language (Literal["en", "es", "nl", "fr", "de", "it", "ro", "pt", "tr"], optional): Language for the exam. Default is "es".
    title (str or None, optional): Title of the exam. Default is None.
    course (str or None, optional): Optional course number. Default is None.
    institution (str or None, optional): Name of the institution. Default is None.
    logo (str or None, optional): Path to a logo image. If the logo is not found, it is simply omitted. Default is None.
    date (str or None, optional): Date of the exam. Default is None.
    replacement (bool or None, optional): Specify whether a replacement exam sheet should be included. Default is None.
    intro (str or Sequence[str] or None, optional): Either a single string with the path to a .tex file or a vector with LaTeX code
        for optional introduction text on the first page of the exam. Default is None.
    blank (int or None, optional): Number of blank pages to be added at the end. Default is None.
    duplex (bool or None, optional): Specify whether blank pages should be added after the title page (for duplex printing). Default is None.
    pages (str or Sequence[str] or None, optional): Path(s) to additional PDF pages to be included at the end of the exam
        (e.g., formulary or distribution tables). Default is None.
    usepackage (str or Sequence[str] or None, optional): Name(s) of additional LaTeX packages to be included. Default is None.
    startid (int or None, optional): Starting ID for the exam numbers (defaults to 1). Default is None.
    showpoints (bool or None, optional): Specify whether the PDF should be shown the number of points associated with each exercise (if specified in the 
        Rnw/Rmd exercise or in points). Default is None.
    samepage (bool or None, optional): Specify whether the itemized question lists should be forced to be on the same page. Default is None.
    twocolumn (bool or None, optional): Specify whether a two-column layout should be used. Default is None.
    reglength (int or None, optional): Number of digits in the registration ID. The default is 7 and it can be increased up to 10.
        In case of reglength < 7, internally reglength = 7 is enforced (and thus necessary in the registration CSV file) but the 
        initial ID digits are fixed to 0 in the exam sheet and corresponding boxes ticked already. Default is None.
    
    rds (bool or None, optional): Logical indicating whether the return list should also be saved as an RDS (R Data Serialization) file.
        Default is None.
    
    **kwargs (optional): Additional parameters. See `exams2nops` (R/exams' documentation) for more details. *Strings must be quoted*.

  Returns:
      None or dict: If return_metadata is True, returns metadata information. Otherwise, returns None.
  """
  __create_dir(odir) 
  __create_dir(tdir)
  __create_dir(sdir)
  __create_dir(texdir)

  pkwargs = {k: __RawParam(v) for k, v in kwargs.items()}
    
  return __render("nops", exercise_templates,
      return_metadata = return_metadata, verbose = verbose, 
      name = name, 
      n = n, nsamp = nsamp, gseed = gseed, seed = seed, 
      exshuffle = exshuffle, points = points, nchoice = nchoice,
      template = template, inputs = inputs, header = header, 
      texengine = texengine, attachfile = attachfile, 
      dir = odir, edir = edir, tdir = tdir, sdir = sdir, texdir = texdir, 
      language = language, title = title, course = course, 
      institution = institution, logo = logo, date = date, 
      replacement = replacement, intro = intro, blank = blank, duplex = duplex, 
      pages = pages, usepackage = usepackage, startid = startid, 
      showpoints = showpoints, samepage = samepage, 
      twocolumn = twocolumn, reglength = reglength, 
      rds = rds, 
      **pkwargs)

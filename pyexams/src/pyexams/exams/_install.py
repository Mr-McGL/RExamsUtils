# -*- coding: utf-8 -*-
# ToDo

# Install rpy2 + versión check
#def install_rpy2(rpy2ver: str | None = None):
#
#  print(f"\x1B[1m\x1B[4m\x1b[34mrpy2 check\x1b[0m")
#
#  rpy2found = find_spec("rpy2") is not None
#
#  if rpy2found and rpy2ver is not None:
#    if get_version(pkg_version("rpy2")) != get_version(rpy2ver):
#      print(f"\x1B[1m\x1b[32mInstalling the selected version: {rpy2ver}.\x1b[0m")
#      run(f"pip install rpy2=={rpy2ver}")
#      reboot()
#      return False
#
#    else:
#      print(f"\x1B[1m\x1b[32mThe selected version is already installed: {rpy2ver}.\x1b[0m")
#
#  elif rpy2found:
#    if get_version(pkg_version("rpy2")) > get_version("3.5.1"):
#      print("\x1B[1m\x1b[31mTo avoid any potential issues with newer versions,\nrpy2 will be downgraded to version 3.5.1 (rpy2=={pkg_version('rpy2')})\x1b[0m")
#      run(f"(pip install rpy2==3.5.1)")
#      reboot()
#      return False
#
#    else:
#      print(f"\x1B[1m\x1b[32mThe current version of the rpy2 package is correct (rpy2=={pkg_version('rpy2')}).\x1b[0m")
#
#  print(f"\x1B[1m\x1B[4m\x1b[34m\nLoading rpy2 extension\x1b[0m")
#  reload_ext("rpy2.ipython")
#
#
## Install R/examas
#def install_rexams(demo_path: str | None = None, rdev:bool = False,
#                   nops_support: bool = True, pypandoc: bool = True,
#                   jedi: bool = True, qti_demo = False):
#  print(f"\x1B[1m\x1B[4m\x1b[34m\nInstalling R/exams\x1b[0m", flush=True)
#  if not rdev:
#    run_R('install.packages("exams", dependencies = TRUE)')
#  else:
#    run_R('install.packages("exams", repos = "https://R-Forge.R-project.org")')
#
#  print(f"\x1B[1m\x1B[4m\x1b[34m\nInstalling TinyTeX for supporting PDF files\x1b[0m")
#  run_R('tinytex::install_tinytex()')
#
#  if nops_support:
#    print(f"\x1B[1m\x1B[4m\x1b[34m\nInstalling packages for NOPS support.\x1b[0m")
#    run("apt-get install pdftk imagemagick")
#
#  if pypandoc:
#    print(f"\x1B[1m\x1B[4m\x1b[34m\nInstalling PyPandoc.\x1b[0m")
#    run("pip install pandoc -U")
#
#  if jedi:
#    print(f"\x1B[1m\x1B[4m\x1b[34m\nInstalling JEDI.\x1b[0m")
#    run("pip install jedi")
#
#  print(f"\x1B[1m\x1B[4m\x1b[34m\nImporting exams into the R environment.\x1b[0m")
#  run_R('library("exams")')
#
#  if demo_path is not None:
#    if not os.path.exists(demo_path):
#      os.makedirs(demo_path)
#
#    print(f"\x1B[1m\x1B[4m\x1b[34m\nInstalling demo files at: '{demo_path}'.\x1b[0m")
#    writers = '"exams2html", "exams2pdf", "exams2moodle"'
#    if nops_support: writers += ', "exams2nops"'
#    if qti_demo: writers += ', "exams2qti12", "exams2qti21"'
#
#    run_R(f'exams_skeleton(dir = "{demo_path}", markup = "markdown", writer = c({writers}));')
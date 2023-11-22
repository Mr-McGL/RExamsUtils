#https://peps.python.org/pep-0621/

#This variables will be destroy at the en of the file
_na             = "N.A."
_lGetName       = lambda author_email: author_email[0:author_email.find("<")-1]\
                    if author_email.find("<") != -1 else ""
_lGetEmail      = lambda author_email: author_email[author_email.find("<")+1:-1]\
                    if author_email.find("<") != -1 else author_email

try:
  from importlib import metadata as __dl_metadata
  _md = __dl_metadata.metadata("nbutils")
  del __dl_metadata
except:
  _md = {}

__metadata__    = _md

__name__        = _md.get("Name",_na)
__version__     = _md.get("Version", _na)
__date__        = "2023/11/13" ############################################
__status__      = [v for k,v in _md.items()\
                      if k == "Classifier" and "Development Status ::" in v]
__status__      = _na if len(__status__) == 0 else __status__[0][22:]


__author__      = _lGetName(_md.get("Author-email", ""))
__maintainer__  = _lGetName(_md.get("Maintainer-email", ""))
__email__       = _lGetEmail(_md.get("Maintainer-email", _na))
__authors__     = [_lGetName(v)  for k,v in _md.items() \
                      if k == "Author-email" and _lGetName(v) != ""] 
__maintainers__ = [_lGetName(v)  for k,v in _md.items() \
                      if k == "Maintainer-email" and _lGetName(v) != ""] 
__emails__      = [_lGetEmail(v) for k,v in _md.items() if k == "Maintainer-email"] 

if __author__     == "": __author__     = _md.get("Author", _na)
if __maintainer__ == "": __maintainer__ = _md.get("Maintainer", _na)
__authors__       = __authors__     + [v for k,v in _md.items() if k == "Author"]
__maintainers__   = __maintainers__ + [v for k,v in _md.items() if k == "Maintainer"]

__copyright__     = "Copyright 2023 VG-lab. All rights reserved" \
        if __author__ == _na else \
                    f"Copyright 2023 VG-lab, {__author__}. All rights reserved"
__license_file__  = _md.get("License-File", _na)
__license__       = [v for k,v in _md.items()\
                      if k == "Classifier" and "License ::" in v]
__license__       = _na if len(__license__) == 0 else __license__[0][11:]

__credits__     = []
__links__       = [v for k,v in _md.items() if k == "Project-URL"]

del _md
del _lGetName
del _lGetEmail
del _na
 


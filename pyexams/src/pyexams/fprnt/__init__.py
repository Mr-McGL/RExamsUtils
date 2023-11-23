# -*- coding: utf-8 -*-
''' Formatted Print Utils
It extends the functionality of the standard "print" function.

EXAMPLE:
  ```
  fprntNNL("Pinta esto de rojo","16",25, fg="r",bg=255)
  print (" ", setFormat("biu",("bg",0,0,255), ("fg","red")) + "25")
  ```

TODO: 
    * special operations: https://notes.burke.libbey.me/ansi-escape-codes/

'''

from  ._fprnt import (format, fgColor, bgColor, special, 
                      fprnt, fprntNNL, 
                      fgvColor, bgvColor, fgRGB, bgRGB,
                      setFormat)



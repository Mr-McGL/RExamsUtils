import io as __dl_io
from ..types import ConstStruct as __cs

####
format = __cs({ 
  "reset"     : '\x1b[0m', #turn off all attributes
  "bold"      : '\x1b[1m',
  "faint"     : '\x1b[2m', #do not work
  "italic"    : '\x1b[3m',  
  "underline" : '\x1b[4m',
  "blink"     : '\x1b[5m', #do not work
  "invrse"    : '\x1b[7m', #do not work
  "hidden"    : '\x1b[8m', #do not work
  "strike"    : '\x1b[9m', #do not work
 
  "resetBold"      : '\x1b[21m',
  "resetItalic"    : '\x1b[23m',  
  "resetUnderline" : '\x1b[24m',

  #Shortcuts
  "rst" : '\x1b[0m',
  "r"   : '\x1b[0m',
  "b"   : '\x1b[1m',
  "i"   : '\x1b[3m',  
  "u"   : '\x1b[4m',
  "rb"  : '\x1b[21m',
  "ri"  : '\x1b[23m',  
  "ru"  : '\x1b[24m',

  #Shortcuts
  "biu" : '\x1b[1m\x1b[3m\x1b[4m',
  "bi"  : '\x1b[1m\x1b[3m',
  "bu"  : '\x1b[1m\x1b[4m',
  "iu"  : '\x1b[3m\x1b[4m',
})

####
fgColor = __cs({
  "black"   : "\x1b[30m",
  "red"     : "\x1b[31m",
  "green"   : "\x1b[32m",
  "yellow"  : "\x1b[33m",
  "blue"    : "\x1b[34m",
  "magenta" : "\x1b[35m",
  "cyan"    : "\x1b[36m",
  "white"   : "\x1b[37m",
  "default" : "\x1b[39m",  

  "bk" : "\x1b[30m",
  "r"  : "\x1b[31m",
  "g"  : "\x1b[32m",
  "y"  : "\x1b[33m",
  "b"  : "\x1b[34m",
  "m"  : "\x1b[35m",
  "c"  : "\x1b[36m",
  "w"  : "\x1b[37m",
  "d"  : "\x1b[39m",  
  
  "britghtBlack"   : "\x1b[90m",
  "britghtRed"     : "\x1b[91m",
  "britghtGreen"   : "\x1b[92m",
  "britghtYellow"  : "\x1b[93m",
  "britghtBlue"    : "\x1b[94m",
  "britghtMagenta" : "\x1b[95m",
  "britghtCyan"    : "\x1b[96m",
  "britghtWhite"   : "\x1b[97m",
})

####
bgColor = __cs({
  "black"   : "\x1b[40m",
  "red"     : "\x1b[41m",
  "green"   : "\x1b[42m",
  "yellow"  : "\x1b[43m",
  "blue"    : "\x1b[44m",
  "magenta" : "\x1b[45m",
  "cyan"    : "\x1b[46m",
  "white"   : "\x1b[47m",
  "default" : "\x1b[49m",  

  "bk" : "\x1b[40m",
  "r"  : "\x1b[41m",
  "g"  : "\x1b[42m",
  "y"  : "\x1b[43m",
  "b"  : "\x1b[44m",
  "m"  : "\x1b[45m",
  "c"  : "\x1b[46m",
  "w"  : "\x1b[47m",
  "d"  : "\x1b[49m",  
  
  "britghtBlack"   : "\x1b[100m",
  "britghtRed"     : "\x1b[101m",
  "britghtGreen"   : "\x1b[102m",
  "britghtYellow"  : "\x1b[103m",
  "britghtBlue"    : "\x1b[104m",
  "britghtMagenta" : "\x1b[105m",
  "britghtCyan"    : "\x1b[106m",
  "britghtWhite"   : "\x1b[107m",
})

####    
special = __cs({
  "cback":"\b",
  "lup":"\x1B[A",
  "lbeging":"\r",
  "lupbegin":"\x1B[F",
  "ldelete": "\x1B[2K!"
})

####
def fprnt(*args, fg = None, bg = None, frmt = None,  **kwargs):
    '''
    Formatted print
    '''
    frmtStr = ""
    if isinstance(fg, (tuple, list)) and len(fg): 
      frmtStr = frmtStr + fgRGB(*fg)
    elif isinstance(fg, int):
      frmtStr = frmtStr + fgvColor(fg)
    else: 
      frmtStr = frmtStr + fgColor.get(fg,"")

    if isinstance(bg, (tuple, list)) and len(bg): 
      frmtStr = frmtStr + bgRGB(*bg)
    elif isinstance(bg, int):
      frmtStr = frmtStr + bgvColor(bg)
    else: 
      frmtStr = frmtStr + bgColor.get(bg,"")
    
    frmtStr = frmtStr + format.get(frmt,"")

    file = kwargs.pop("file", None)
    end = kwargs.pop("end", None)
    flush = kwargs.pop("flush", None)
    op = __dl_io.StringIO()
    print(*args, file = op, end = '', **kwargs)
    string = op.getvalue()
    op.close()

    string = frmtStr + string + format['r']
    
    print(string, flush = flush, file = file, end = end)

####
def fprntNNL(*args, **kwargs):
  '''
  Formatted print (no new line)
  '''
  kwargs.pop("end", None)
  fprnt(*args, end = '', **kwargs)                                                      

####
def fgvColor(c):
  ''' c = [0 - 255] '''
  return f'\x1b[38;5;{c}m'

####
def bgvColor(c):
  ''' c = [0 - 255] '''
  return f'\x1b[48;5;{c}m'

####
def fgRGB (r,g,b): return f'\x1b[38;2;{r};{g};{b}m'
def bgRGB (r,g,b): return f'\x1b[48;2;{r};{g};{b}m'

####
def setFormat(*args):
  frmt = ""
  for f in args:
    if isinstance(f, (tuple, list)) and len(f) == 4 and\
      f[0]=="fg" and all(isinstance(v, int) for v in f[1:]):
        frmt = frmt + fgRGB(*(f[1:]))
    elif isinstance(f, (tuple, list)) and len(f) == 4 and\
      f[0]=="bg" and all(isinstance(v, int) for v in f[1:]):
        frmt = frmt + bgRGB(*(f[1:]))
    elif isinstance(f, (tuple, list)) and len(f) == 2 and\
      f[0]=="fg" and isinstance(f[1], int):
        frmt = frmt + fgvColor(f[1])
    elif isinstance(f, (tuple, list)) and len(f) == 2 and\
      f[0]=="bg" and isinstance(f[1], int):
        frmt = frmt + bgvColor(f[1])
    elif isinstance(f, (tuple, list)) and len(f) == 2 and\
      f[0]=="fg" and isinstance(f[1], str):
        frmt = frmt + fgColor.get(f[1],"")
    elif isinstance(f, (tuple, list)) and len(f) == 2 and\
      f[0]=="bg" and isinstance(f[1], str):
        frmt = frmt + bgColor.get(f[1],"")
    elif isinstance(f, str):
      if   f[0:2] == "fg": frmt = frmt + fgColor.get(f[2:],"")
      elif f[0:2] == "bg": frmt = frmt + bgColor.get(f[2:],"")
      elif f[0:2] == "sp": frmt = frmt + special.get(f[2:],"")
      else: frmt = frmt + format.get(f,"")
  return frmt



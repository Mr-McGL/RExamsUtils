#TODO:
# * Run them all at start

def runningInColab():  
  return 'colab' in get_ipython().parent_header["metadata"]

#from google.colab import _message
#def runningInColab():
  #return _message.blocking_request('get_ipynb', timeout_sec=2) is not None

def runningInRemoteColab():  
  return 'google.colab' in str(get_ipython())
  #return 'google.colab' in str(get_ipython()) if hasattr(__builtins__,'__IPYTHON__') else False


def runningInLocalColab():
  return runningInColab() and not runningInRemoteColab()

def isColabToolkitInstalled():
  try:  
    import google.colab as ___gct___
    del ___gct___
    return True
  except: 
    return False
#Simple Struct
#class Struct:
#  def __init__(self, **entries): self.__dict__.update(entries)
#  def __getitem__(self, key): return self.__dict__[key]
#  # Ducking (dict)
#  # def values(self, *args, **kwargs): return self.__dict__.values(*args,**kwargs)
#  # '__contains__', '__delitem__',	'__iter__',	'__len__',	'__reversed__',	
#  # '__setitem__',	'clear', 'copy', 'fromkeys',	 'get',	 'items',	 'keys',
#  # 'pop', 'popitem', 'setdefault', 'update', 'values'

import threading as _dl_threading

class LockFunc():
  def __init__(self):
    self.__lock = _dl_threading.Lock()
  
  def func(self, func, args = (), kwargs = {}):
    self.acquire()
    try: 
      func(*args, **kwargs)
    finally: 
      self.release()
  
  def acquire(self): self.__lock.acquire()
  def release(self): self.__lock.release()



class Struct(dict): 
  def __getattr__(self, name): return self[name]
  def __setattr__(self, name, value): self[name] = value


class ConstStruct(Struct): 
  def __setitem__(self, key, value):
    if key not in self:
      raise KeyError('No new keys allowed')
    else:
      raise KeyError('Constant value cannot be override')

class FixStruct(Struct): 
  def __setitem__(self, key, value):
    if key not in self:
      raise KeyError('No new keys allowed')
    else:
      super().__setitem__(key, value)


class ListStruct(FixStruct):
  def __init__(self, n, prefix = 'i',val = None): 
    d = dict()
    for i in range(n): d[f'{prefix}{i}'] =val
    super().__init__(d)

  def getList(self):
    return list(self.values())


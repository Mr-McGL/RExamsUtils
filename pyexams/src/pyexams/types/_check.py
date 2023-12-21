from typing import Sequence, Type, Any, cast

_BasicTypes = Type[int] | Type[float] | Type[complex] | Type[str] | Type[bool] #allready includes: bool(int)

def is_seq(val: Any, types: _BasicTypes | Sequence[_BasicTypes]):
  """
  Check if the given value is a sequence of the specified type or types.

  Args:
      val (Any): The value to check.
      types (BasicTypes | Sequence[BasicTypes]): The type or types of the sequence elements.

  Returns:
      bool: True if the value is a sequence of the specified types, False otherwise.

  Example:

      >>> is_seq([1, 2, 3], int)
      True
      >>> is_seq("abc", str)
      False
      >>> is_seq([1, "abc", True], (int, str, bool))
      True
  """
  if isinstance(val, str): 
    return False
  elif isinstance(val, Sequence):
    return all(isinstance(item, cast(type, types)) for item in val)
  
  return False

###

def is_seq_of_seq(val: Any, types: _BasicTypes | Sequence[_BasicTypes]):
  if isinstance(val, str): 
    return False
  elif isinstance(val, Sequence): 
    return all(is_seq(item, types) for item in val)
  
  return False

###

def is_seq_of_seq_or_bt(val: Any, types: _BasicTypes | Sequence[_BasicTypes]):
  """
  Check if the given value is a sequence of sequences of the specified type or types, or a sequence of basic types.

  Args:
      val (Any): The value to check.
      types (BasicTypes | Sequence[BasicTypes]): The type or types of the sequence elements.

  Returns:
      bool: True if the value is a sequence of sequences of the specified types or a sequence of basic types, False otherwise.

  Example:

      >>> is_seq_of_seq_or_bt([[1, 2, 3], [4, 5, 6]], int)
      True
      >>> is_seq_of_seq_or_bt("abc", str)
      True
      >>> is_seq_of_seq_or_bt([[1, "abc", True], 4, 5, 6], (int, str, bool))
      True
  """
  if isinstance(val, str): 
    return False
  elif isinstance(val, Sequence): 
    return all(isinstance(item, cast(type, types)) or is_seq(item, types) for item in val)
  
  return False

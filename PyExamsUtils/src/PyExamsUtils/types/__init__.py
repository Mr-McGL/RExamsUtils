# -*- coding: utf-8 -*-
''' Additional types

Types:
  * Struct: Attributes are dictionary keys
  * FixStruct: New values cannot be added
  * ConstStruct: Values cannot be modified
  * ListStruct

TODO:
  * Check other struct implementations.
  * Create __dict__ to use vars!
  * Add __deepcopy__
'''

from ._types import LockFunc, Struct, ConstStruct, FixStruct, ListStruct
from ._functions import remove_copies

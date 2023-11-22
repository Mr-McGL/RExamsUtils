def remove_copies(lst: list):
  """Remove duplicate elements from a list while preserving the order.

  This function takes a list and removes duplicate elements from it while
  maintaining the order of the remaining elements.

  Parameters:
      lst (list): The input list with possible duplicate elements.

  Returns:
      list: A list with duplicates removed and the original order preserved.

  Usage:
      remove_copies([1, 2, 2, 3, 4, 4, 5])
  """
  return list(sorted(set(lst), key=lst.index))
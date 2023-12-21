def print_metadata(meta_data: dict) -> None:
  """
  Print metadata information from a dictionary containing exercise data.

  Parameters:
      meta_data (dict): A dictionary containing metadata information for exercises.

  Prints:
      None

  The function iterates over the items in the input dictionary, assuming it has a structure where the keys represent exams and the values are dictionaries containing information about exercises. For each exam, it prints the exam name and then iterates over the exercises within that exam, printing the exercise number, name, and associated string information.

  Example:
  --------
  meta_data = {
      'exam1': {
          'exercise1': {'string': 'Swiss Capital: b'}, # ... (other values)
          'exercise2': {'string': 'Analysis of variance: a, c, d'}, # ... (other values)
          # ... (other exercises)
      },
      'exam2': {
          'exercise1': {'string': 'Swiss Capital: c'}, # ... (other values)
          'exercise2': {'string': 'Analysis of variance: c, d'}, # ... (other values)
          # ... (other exercises)
      },
      # ... (other exams)
  }

  Usage:
  ------
  print_metadata(meta_data)
  """
  for exam, exercises in meta_data['exams'].items():
    print(f'{exam}:')
    for i, (name, exercise) in enumerate(exercises.items()):
      print(f"    {i+1}. {exercise['string']}")
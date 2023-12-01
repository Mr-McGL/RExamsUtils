#https://stackoverflow.com/questions/279561/what-is-the-python-equivalent-of-static-variables-inside-a-function
def static_vars(**kwargs):
  """
  Decorator function to add static variables to a function.

  Usage:
  @static_vars(var1=value1, var2=value2, ...)
  def your_function(...):
      # Function code

  Parameters:
  - **kwargs: Keyword arguments where the keys are variable names
              and the values are their corresponding initial values.

  Returns:
  A decorator that adds the specified static variables to the decorated function.

  Example:
  @static_vars(counter=0, is_active=True)
  def example_function():
    if example_function.is_active:
      print(example_function.counter)
      example_function.counter += 1
  """
  def decorate(func):
    for k in kwargs:
      setattr(func, k, kwargs[k])
    return func
  return decorate
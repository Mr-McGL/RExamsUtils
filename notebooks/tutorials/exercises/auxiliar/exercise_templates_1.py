# -*- coding: utf-8 -*-
# ToDo:
# * Standardize headers.
# * Homogenizar cabezeras.

# References:
# https://ipywidgets.readthedocs.io/en/7.6.4/examples/Widget%20Styling.html#The-Flexbox-layout

import ipywidgets as widgets
from IPython.display import display

class GridOutput(widgets.Widget):
  """
  Custom widget for displaying a grid of Output widgets.

  Parameters:
  - nrows (int): Number of rows in the grid.
  - ncols (int): Number of columns in the grid.
  - width (str, optional): Width of the grid.
  - max_height (str, optional): Maximum height of each output widget.

  Example usage:
  nrows, ncols = 2, 3
  grid_widget = GridOutput(nrows, ncols, width="50%", max_height="100px")

  for o in grid_widget:
      with o:
          for i in range(4):
              print(i)

  for i in range(nrows):
      for j in range(ncols):
          with grid_widget[i, j]:
              print(f"---{i, j}---")

  for i in range(nrows * ncols):
      with grid_widget[i]:
          print(f"---{i}---")
  display(grid_widget)
  """
  def __init__(self, nrows: int, ncols: int, width: str="100%", max_height: str="auto" ):
    super().__init__()

    if nrows <= 0 or ncols <= 0:
      raise ValueError("Number of rows and columns must be greater than zero.")

    self._outputs = [widgets.Output() for i in range(nrows*ncols)]

    itemlt = widgets.Layout(width='auto', height='auto', max_height=max_height)  #border='3px solid black'
    items =[widgets.VBox([o], layout=itemlt) for o in self._outputs]

    self._gbox = widgets.GridBox(
      children = items,
      layout=widgets.Layout(width=width,
            grid_template_columns=" ".join(["1fr"] * ncols), 
            grid_template_rows=" ".join(["auto"] * nrows),
            grid_gap='10px 10px')) #border='1px solid black'

    self._nrows = nrows
    self._ncols = ncols

  def _ipython_display_(self, **kwargs):
    """
    Called when the widget is displayed in IPython.
    """
    display(self._gbox, **kwargs)

  def __getitem__(self, key):
    """
    Enables indexing to get outputs using a global index or a tuple of row and column.

    Parameters:
    - key (int or tuple): Global index or a tuple of row and column indices.

    Returns:
    - widget.Output: The Output widget at the specified location.

    Raises:
    - ValueError: If the index is not an integer or a tuple of two integers.
                  If the index is out of range.
    """
    # ToDo: Range check
    if isinstance(key, tuple) and len(key) == 2 and all(isinstance(i, int) for i in key):
      return self._outputs[key[0]*self._ncols + key[1]]
    elif isinstance(key, int):
      return self._outputs[key]

    raise ValueError("Index must be an integer or tuple of two integers.")

  def __iter__(self):
    return iter(self._outputs)
  

class DropdownConfirm(widgets.Widget):
  """
  Custom widget combining a Dropdown and Button for user interaction.

  Parameters:
  - options (list): List of options for the Dropdown.
  - callback (callable, optional): Custom callback function to execute on Button click.
  - dlabel (str, optional): Label for the Dropdown.
  - blabel (str, optional): Label for the Button.
  - layout (ipywidgets.Layout, optional): Layout configuration for the widget.

  Example Usage:
  options_list = ['Option 1', 'Option 2', 'Option 3']
  dropdown_confirm = DropdownConfirm(options=options_list, callback=my_callback_function,
                                    dlabel='Select an option:', blabel='Run', layout=my_layout)
  display(dropdown_confirm)
  """
  def __init__(self, options, callback=None,
               dlabel = 'Select an option:', blabel='Run', layout=None):
    super().__init__()

    if not options:
      raise ValueError("Options list cannot be empty.")

    self._options = options
    self._callback = callback

    self._dropdown = widgets.Dropdown(options=options, description=dlabel, style={'description_width': 'initial'})
    self._button = widgets.Button(description=blabel)
    self._button.on_click(self._on_button_click)

    lt = layout if layout else widgets.Layout()
    self._layout = widgets.HBox([self._dropdown, self._button], layout=lt)

  def set_cb(self, callback=None):
    """
    Set the callback function for button click.

    Parameters:
    - callback (callable, optional): Custom callback function to execute on Button click.
    """
    self._callback = callback

  def _on_button_click(self, b):
    """
    Called when the button is clicked.

    Parameters:
    - b: The button instance.
    """
    if self._callback: self._callback(self._dropdown.value)
  
  def _ipython_display_(self, **kwargs):
    """
    Called when the widget is displayed in IPython.
    """
    display(self._layout, **kwargs)


class GridOutputAndDropdownConfirm(widgets.Widget):
  """
  Custom widget combining GridOutput and DropdownConfirm.

  Parameters:
  - nrows (int): Number of rows in the grid.
  - ncols (int): Number of columns in the grid.
  - options (list): List of options for the Dropdown.
  - output_list_callback (callable, optional): Callback for handling the list of output widgets.
  - single_output_callback (callable, optional): Callback for handling a single output widget.
  - gwidth (str, optional): Width of the grid.
  - gmaxheight (str, optional): Maximum height of each output widget in the grid.
  - dlabel (str, optional): Label for the Dropdown.
  - dblabel (str, optional): Label for the Button in the Dropdown.
  - dlayout (ipywidgets.Layout, optional): Layout configuration for the Dropdown.
  """
  def __init__(self, nrows, ncols, options, 
               output_list_callback=None, single_output_callback=None,
               gwidth = "100%", gmaxheight="auto",
               dlabel = 'Select an option:', dblabel='Run', dlayout=None):
    super().__init__()
  
    self._nrows = nrows
    self._ncols = ncols
    self._output_list_callback = output_list_callback 
    self._single_output_callback= single_output_callback
    self._dropdown_confirm=DropdownConfirm(options=options, callback=self._on_button_click, 
                dlabel=dlabel,blabel=dblabel,layout=dlayout)
    self._grid_widget=GridOutput(nrows, ncols, width = gwidth, 
                max_height = gmaxheight)
  
  def _on_button_click(self, selected_val):
    if self._single_output_callback:
      for i in range(self._nrows):
        for j in range(self._ncols):
          self._single_output_callback(selected_val, self._grid_widget[i,j],i,j)

    if self._output_list_callback:
      self._output_list_callback(selected_val, list(self._grid_widget),self._nrows, self._ncols)
    
    
  def set_output_list_cb(self, callback=None):
    """
    Set the callback function for handling the list of output widgets.

    Parameters:
    - callback (callable, optional): Custom callback function.
    """
    self._output_list_callback = callback
    
  def set_single_output_cb(self, callback=None):
    """
    Set the callback function for handling a single output widget.

    Parameters:
    - callback (callable, optional): Custom callback function.
    """
    self._single_output_callback = callback
  
  def _ipython_display_(self, **kwargs):
    """
    Called when the widget is displayed in IPython.
    """
    display(self._dropdown_confirm, self._grid_widget, **kwargs)

########################
# Test 1
########################
#nrows, ncols = 2, 3
#grid_widget = GridOutput(nrows, ncols, width="50%", max_height = "100px")
#
#for o in grid_widget:
#  with o:
#    for i in range(4): print(i)
#
#for i in range(nrows):
#  for j in range(ncols):
#    with grid_widget[i,j]:
#      print(f"---{i, j}---")
#
#for i in range(nrows*ncols):
#  with grid_widget[i]:
#    print(f"---{i}---")
#
#display(grid_widget)

########################
# Test 2
########################
#options_list = ['Option 1', 'Option 2', 'Option 3']
#dropdown_confirm = DropdownConfirm(options=options_list)
#display(dropdown_confirm)

########################
# Test 3
########################
#from IPython.display import clear_output
#nrows, ncols = 2, 3
#options_list = ['Option 1', 'Option 2', 'Option 3']
#
#dropdown_confirm = DropdownConfirm(options=options_list)
#grid_widget = GridOutput(nrows, ncols, width="50%", max_height = "100px")
#
#def print_val(val):
#  for o in grid_widget:
#    with o:
#      clear_output()
#      print(val)
#
#dropdown_confirm.set_cb(print_val)
#
#display(dropdown_confirm, grid_widget)

########################
# Test 4
########################
#def print_cb(val, output, i, j): 
#  with output:
#    print (f'____{i,j, val}____')
#
#def print2_cb(val, outputs, *args): 
#  for output in outputs:
#    with output:
#      print (f'____{val}____')
#
#
#options_list = ['Option 1', 'Option 2', 'Option 3']
#display(GridOutputAndDropdownConfirm(2,3, options=options_list, 
#                                     single_output_callback=print_cb, 
#                                     output_list_callback=print2_cb,
#                                     gmaxheight="40px"))


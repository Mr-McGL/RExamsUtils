# -*- coding: utf-8 -*-
# ToDo:
# * Standardize headers.

# References:
# https://ipywidgets.readthedocs.io/en/7.6.4/examples/Widget%20Styling.html#The-Flexbox-layout

import os
import tempfile
import shutil

import ipywidgets as widgets
from IPython.display import clear_output, display

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name, get_all_styles

from pyexams.exams import toPDF
from pyexams.ex import run as _run


try:
  from pdf2image import convert_from_path
except:
  _run("pip install pdf2image")
  _run("sudo apt-get install poppler-utils")
  from pdf2image import convert_from_path

def PDF(fn):
  """
  Display a PDF file.

  Parameters:
  - fn (str): Path to the PDF file.
  """
  images = convert_from_path(fn)
  for img in images:
    display(img)


def invert_color(hc):
  """
  Invert the color represented by a hexadecimal code.

  Parameters:
  - hc (str): Hexadecimal color code.

  Returns:
  - str: Inverted hexadecimal color code.
  """
  res = ''.join(f'{255-int(hc[i:i+2],16):02X}' for i in range(1, len(hc), 2))
  return f'#{res}'


class SyntaxHighlighter(widgets.VBox): ## ToDo: Check how to extend
  """
  Widget for syntax highlighting code.

  Parameters:
  - lexer (str, optional): The name of the lexer to use (default is 'markdown').
  - style (str, optional): The name of the style to use (default is 'dracula').
  - initial_text (str, optional): Initial code in the editor.
  - height (str, optional): Height of the widget.

  Example Usage:
  syntax_highlighter = SyntaxHighlighter(lexer='python', style='monokai', initial_text='print("Hello, World!")')
  display(syntax_highlighter)
  """
  def __init__(self, lexer:str='markdown', style:str= 'dracula', initial_text:str='', height: str='auto'): #max_heigth = 'auto'
    self._lexer = get_lexer_by_name(lexer) #, stripall=True)
    self._style = get_style_by_name(style)

    self._editor = widgets.Textarea(
      value = initial_text,
      placeholder='Type your code here...',
      layout={'width':'99%', "height":"99%"}#, 'max_height': max_heigth}# 'font_family': 'Monaco, monospace', 'font_size': '20px'}
    )

    self._highlighted = widgets.HTML(layout={'width':'99%', "height":"99%"})
    self._style_dd = widgets.Dropdown(options=list(get_all_styles()), value=style, description='Style:')
    self._invertbg = widgets.Button( description='Invert Background Color')


    self._tabs = widgets.Tab(children=[self._editor,
                                       widgets.VBox([widgets.HBox([self._style_dd,
                                                                   self._invertbg]),
                                                     self._highlighted])],#ToDo: Fijar el selector de estilos!.
                             layout={'height':"99%"})
    self._tabs.set_title(0, 'Editor')
    self._tabs.set_title(1, 'Highlighted Syntax')

    self._update_syntax()
    self._editor.observe(self._update_syntax, names='value')
    self._style_dd.observe(self._update_style, names='value')
    self._invertbg.on_click(self._invert_background)

    super().__init__([self._tabs],layout={'height':height})

  def _update_syntax(self, *args):
    try:
      formatter = HtmlFormatter(style=self._style, noclasses=True)# linenos=True)
      highlighted_code = highlight(self._editor.value, self._lexer, formatter)
      self._highlighted.value = highlighted_code # f'<pre style="color:#333333; background-color:#f8f8f8; padding:10px;">{highlighted_code}</pre>'

    except Exception as e:
      print(f"Error highlighting code: {e}")

  def _update_style(self, *args):
    self._style = get_style_by_name(self._style_dd.value)
    self._update_syntax()

  def get_value(self):
    """
    Get the current value of the editor.

    Returns:
    - str: The code in the editor.
    """
    return self._editor.value

  def _invert_background(self, *args):
    self._style.background_color = invert_color(self._style.background_color)
    self._update_syntax()


class QuestionBuilder(widgets.Widget):
  """
  Widget for building exam questions.

  Parameters:
  - initial_text (str, optional): Initial text for the editor.

  Example Usage:
  question_builder = QuestionBuilder(initial_text='# Question\n\nWrite your answer here.')
  display(question_builder)
  """
  def __init__(self, initial_text=''):
    super().__init__()

    self._render_bt = widgets.Button(description="Render - Rebuild Question", layout={'width':'auto'})
    self._editor = SyntaxHighlighter(initial_text=initial_text, height='95%')
    self._render_out = widgets.Output()
    self._console = widgets.Output()

    self._layout = widgets.VBox(
        [ widgets.VBox([self._render_bt], layout={'display':'flex', 'flex_flow':'row', 'align_items':'stretch'}),
          widgets.HBox(
            [ widgets.VBox([ widgets.HTML("<h2>Exercise Template</h2>"), self._editor],
                           layout={'flex': '1', 'height':'100%'}),
              widgets.VBox([ widgets.HTML("<h2>Exam</h2><br>"),
                             widgets.VBox([self._render_out], layout={'height':'100%'})],
                           layout={'flex': '1','height':'100%'})],
            layout={'height':'450px'}),
          widgets.HTML("<h2>Console</h2>"),
          widgets.VBox([self._console], layout={"height":"100px"})],
        layout={'width':'100%'})

    #self._on_button_click()
    self._render_bt.on_click(self._on_button_click)

  def _on_button_click(self, *args):
    with self._console:
      fn = "test"
      folder = tempfile.mkdtemp(prefix="rexamstmp_")
      with open(f"{os.path.join(folder,fn)}.Rmd",'w') as f:
        f.write(self._editor.get_value())
      toPDF(f"{fn}.Rmd", name="test", odir=folder, edir=folder, verbose='low');

    with self._render_out:
      clear_output(wait = True)
      display(PDF(f"{os.path.join(folder,fn)}1.pdf"))
    with self._console:
      shutil.rmtree(folder)

  def _ipython_display_(self, **kwargs):
    display(self._layout, **kwargs)
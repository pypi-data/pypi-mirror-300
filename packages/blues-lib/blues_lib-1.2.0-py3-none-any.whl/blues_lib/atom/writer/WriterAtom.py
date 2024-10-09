from abc import ABC
import sys,os,re

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from atom.Atom import Atom     

class WriterAtom(Atom,ABC):

  _category = 'writer'
  
  def __init__(self,kind,title,selector,value):
    '''
    Create a plain atom instance
    The atom is used to write value into the form controller
    Parameter:
      kind (str) : the atom's kind
      title (str) : the atom's title
      selector (str) : the atom's selector
      value (str) optional: the atom's value
    Returns:
      Atom : a atom instance
    '''
    super().__init__(self._category,kind,title)
    self._selector = selector
    self._value = value
  
  # getter
  def get_selector(self):
    return self._selector
  
  def get_value(self):
    return self._value
  
  # setter
  def set_selector(self,selector):
    self._selector = selector

  def set_value(self,value):
    self._value = value


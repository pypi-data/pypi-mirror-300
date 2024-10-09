from abc import ABC
import sys,os,re

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from atom.Atom import Atom     

class ReaderAtom(Atom,ABC):

  _category = 'reader'
  
  def __init__(self,kind,title,selector,value=None,parent_selector=None):
    '''
    A readable elment 
    Parameter:
      kind (str) : the atom's kind
      title (str) : the atom's description
      selector (str|list) : the element's css selector
      value (str) : the value's meaning base on the concrete atom
      parent_selector {dict} : the extend parent_selector
    Returns:
      BluesAtom : a atom instance
    '''
    super().__init__(self._category,kind,title)
    self._selector = selector
    self._parent_selector = parent_selector
    self._value = value
    self._parent_selector = parent_selector

  # getter
  def get_selector(self):
    return self._selector
  
  def get_value(self):
    return self._value
  
  def get_parent_selector(self):
    return self._parent_selector
  
  # setter
  def set_selector(self,selector):
    self._selector = selector

  def set_value(self,value):
    self._value = value

  def set_parent_selector(self,parent_selector):
    self._parent_selector = parent_selector



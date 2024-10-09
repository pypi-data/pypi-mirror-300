import sys,os,re

sys.path.append(re.sub('test.*','blues_lib',os.path.realpath(__file__)))
from atom.AtomFactory import AtomFactory     
from atom.Atom import Atom
from pool.BluesMaterialIO import BluesMaterialIO

class ReleaserSchema():

  def __init__(self):
    self.atom_factory = AtomFactory()

    # { dict } standard material row
    self.material = None

    # { URLAtom } the form page
    self.url_atom = self.get_url_atom()
    # { ElementAtom } the form page's mark atom
    self.mark_atom = self.get_mark_atom()
    # { list<Atom> } the form controller atom list
    self.fill_atom = self.get_fill_atom()
    # { list<Atom> } the preview atom list
    self.preview_atom = self.get_preview_atom()
    # { list<Atom> } the submit atom list
    self.submit_atom = self.get_submit_atom()
    # { list<Atom> } the modal atom list, should be closed
    self.popup_atom = self.get_popup_atom()

    # fillin the material value
    self.set_material()

  def set_material(self):
    pass
  
  def get_url_atom(self):
    pass

  def get_mark_atom(self):
    pass

  def get_fill_atom(self):
    pass

  def get_preview_atom(self):
    pass

  def get_submit_atom(self):
    pass

  def get_popup_atom(self):
    pass

  def set_fill_value(self,value_dict):
    '''
    Replace the placeholder value in the atom
    Parameter:
      value_dict {dict} : the key is the placeholder, the value is the real value
    '''
    # Only support to replace the atom's vlue
    self.__set_atom_value(self.fill_atom,value_dict)

  def set_preview_value(self,value_dict):
    self.__set_atom_value(self.preview_atom,value_dict)

  def set_submit_value(self,value_dict):
    self.__set_atom_value(self.submit_atom,value_dict)

  def set_modal_value(self,value_dict):
    self.__set_atom_value(self.popup_atom,value_dict)

  def __set_atom_value(self,atom_node,value_dict):
    
    if not atom_node:
      return
    
    # only deal with atom node
    if not isinstance(atom_node,Atom):
      return

    atom_value = atom_node.get_value()

    if isinstance(atom_value,list):
      idx = 0
      for sub_atom_value in atom_value:
        if isinstance(sub_atom_value,Atom):
          self.__set_atom_value(sub_atom_value,value_dict)
        else:
          atom_value[idx] = self.__get_replaced_value(sub_atom_value,value_dict)
        idx+=1
      
    elif isinstance(atom_value,dict):
      for key,sub_atom_value in atom_value.items():
        if isinstance(sub_atom_value,Atom):
          self.__set_atom_value(sub_atom_value,value_dict)
        else:
          atom_value[key] = self.__get_replaced_value(sub_atom_value,value_dict)

    elif isinstance(atom_value,str):
      atom_node.set_value(self.__get_replaced_value(atom_value,value_dict))

  def __get_replaced_value(self,placeholder,value_dict):

    if placeholder in value_dict:
      return value_dict.get(placeholder)
    else:
      return placeholder

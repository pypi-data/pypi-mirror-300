import sys,os,re
from abc import ABC

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from atom.AtomFactory import AtomFactory     

class LoginerSchema(ABC):

  def __init__(self):
    self.atom_factory = AtomFactory()
    # { URLAtom } : the login page url
    self.url_atom = self.get_url_atom()
    # { ElementAtom } : the login page's mark element
    self.mark_atom = self.get_mark_atom()
    # { WordAtom } : the max open waiting time
    self.timeout_atom = self.get_timetout_atom()
    # { WordAtom } : the proxy config
    self.proxy_atom = self.get_proxy_atom()
    # { WordAtom } : the cookie filter config
    self.cookie_filter_atom = self.get_cookie_filter_atom()
    # { list<WordAtom > } : the elements switch to the login page
    self.switch_atom = self.get_switch_atom()
    # { list<WordAtom > } : the fill controllers atom
    self.fill_atom = self.get_fill_atom()
    # { list<WordAtom > } : the fill controllers atom
    self.submit_atom = self.get_submit_atom()

  def get_url_atom(self):
    pass

  def get_mark_atom(self):
    pass

  def get_timetout_atom(self):
    return self.atom_factory.createData('page load timeout',20)

  def get_proxy_atom(self):
    pass

  def get_cookie_filter_atom(self):
    pass
  
  def get_switch_atom(self):
    pass

  def get_fill_atom(self):
    pass

  def get_submit_atom(self):
    pass


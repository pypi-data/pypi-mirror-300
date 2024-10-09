import sys,os,re

sys.path.append(re.sub('test.*','blues_lib',os.path.realpath(__file__)))
from atom.AtomFactory import AtomFactory     

class ReaderSchema():

  def __init__(self):
    self.atom_factory = AtomFactory()

    # { URLAtom } the list page
    self.url_atom = self.get_url_atom()
    # { WordAtom } would crawl materials count
    self.size_atom = self.get_size_atom()
    # { WordsAtom } the author list
    self.author_atom = self.get_author_atom()
    # { WordAtom } the max image count
    self.image_size_atom = self.get_image_size_atom()
    # { ListAtom } the brief atom
    self.brief_atom = self.get_brief_atom()
    # { ArticleAtom } the article atom
    self.material_atom = self.get_material_atom()

  def get_url_atom(self):
    pass

  def get_size_atom(self):
    return self.atom_factory.createData('material size',1)

  def get_author_atom(self):
    pass

  def get_image_size_atom(self):
    return self.atom_factory.createData('max image count',9)

  def get_brief_atom(self):
    pass

  def get_material_atom(self):
    pass


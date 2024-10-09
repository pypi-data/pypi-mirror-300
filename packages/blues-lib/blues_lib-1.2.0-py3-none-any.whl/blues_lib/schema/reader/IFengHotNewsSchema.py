from .IFengNewsSchema import IFengNewsSchema

class IFengHotNewsSchema(IFengNewsSchema):
  
  def get_url_atom(self):
    return self.atom_factory.createURL('ifeng homepage','https://www.ifeng.com/')

  def get_brief_atom(self):
    unit_selector = 'div[class^=index_hot_box] p[class^=index_news_list_p],div[class^=index_hot_box] h3'
    field_atoms = [
      self.atom_factory.createAttr('material_title','a','title'),
      self.atom_factory.createAttr('material_url','a','href'), # get from the unit element
    ]
    array_atom = self.atom_factory.createArray('fields',field_atoms) 
    brief_atom = self.atom_factory.createBrief('briefs',unit_selector,array_atom) 
    return brief_atom

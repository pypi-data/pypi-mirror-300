from .NewsReaderSchema import NewsReaderSchema

class IFengNewsSchema(NewsReaderSchema):
  
  def get_url_atom(self):
    pass

  def get_author_atom(self):
    return self.atom_factory.createData('author list',['凤凰网','凤凰新闻'])

  def get_brief_atom(self):
    pass


  def get_material_atom(self):
    '''
    Create a news material atom
    '''

    # para atom
    para_unit_selector = 'div[class^=index_text] p:not(.picIntro)'
    para_field_atoms = [
      # use the para selector
      self.atom_factory.createText('text',''),
      self.atom_factory.createAttr('image','img','data-lazyload'),
    ]
    para_array_atom = self.atom_factory.createArray('para fields',para_field_atoms) 
    para_atom = self.atom_factory.createPara('material_body',para_unit_selector,para_array_atom) 
    
    # outer atom
    container_selector = 'div[class^=index_leftContent]'
    field_atoms = [
      self.atom_factory.createText('material_title','h1'),
      self.atom_factory.createText('material_post_date','div[class^=index_timeBref] a'),
      para_atom,
    ]
    array_atom = self.atom_factory.createArray('fields',field_atoms) 
    news_atom = self.atom_factory.createNews('news',container_selector,array_atom) 
    return news_atom


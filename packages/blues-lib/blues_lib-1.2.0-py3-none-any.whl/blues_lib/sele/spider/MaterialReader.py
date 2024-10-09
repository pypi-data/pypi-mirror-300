import sys,os,re

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.behavior.BehaviorChain import BehaviorChain
from pool.BluesMaterialIO import BluesMaterialIO  
from util.BluesURL import BluesURL 
from util.BluesConsole import BluesConsole 

class MaterialReader():
  def __init__(self,browser,reader_schema):
    self.browser = browser
    self.reader_schema = reader_schema
    self.__prepare()

  def __prepare(self):
    self.url_atom = self.reader_schema.url_atom
    self.size_atom = self.reader_schema.size_atom
    self.brief_atom = self.reader_schema.brief_atom
    self.material_atom = self.reader_schema.material_atom
    
  def read(self):
    briefs = self.get_briefs()
    if not briefs:
      BluesConsole.error('No briefs')
      return None
    
    briefs = self.__get_available_briefs(briefs)
    if not briefs:
      BluesConsole.error('No available briefs')
      return None

    BluesConsole.success('%s available briefs' % str(len(briefs)))

    mateirals = []
    for brief in briefs:

      try:
        material = self.get_material(brief)

        # weather the detail is legal
        if BluesMaterialIO.is_legal_detail(material):
          mateirals.append({**brief,**material})

      except Exception as e:
        # some detail page is wrong
        BluesConsole.info('Crawl the material (%s), get the next one, error %s' % (brief.get('material_title'),e))
        # write the error log

      # contrl the materail size
      if self.size_atom and len(mateirals) >= self.size_atom.get_value():
        break

    return mateirals

  def get_briefs(self):
    self.browser.open(self.url_atom.get_value())
    handler = BehaviorChain(self.browser,self.brief_atom)
    outcome = handler.handle()
    return outcome.data

  def __get_available_briefs(self,briefs):
    ava_briefs = []
    for brief in briefs:
      self.__extend_brief(brief)
      if not BluesMaterialIO.is_legal_brief(brief):
        continue
      if not BluesMaterialIO.exist(brief):
        ava_briefs.append(brief)
    return ava_briefs

  def __extend_brief(self,brief):
    material_site = BluesURL.get_main_domain(brief['material_url'])
    material_id = material_site+'_'+BluesURL.get_file_name(brief['material_url'])
    brief['material_id'] = material_id
    brief['material_site'] = material_site

  def get_material(self,brief):
    url = BluesMaterialIO.get_material_url(brief)
    print('url',self.material_atom)
    if not url or not self.material_atom:
      BluesConsole.error('Material url or atom is none')
      return None
    BluesConsole.success('Crawling material: %s' % url)
    self.browser.open(url)
    handler = BehaviorChain(self.browser,self.material_atom)
    outcome = handler.handle()
    return outcome.data


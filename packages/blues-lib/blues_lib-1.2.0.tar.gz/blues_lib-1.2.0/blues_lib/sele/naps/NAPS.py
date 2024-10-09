import sys,os,re
from abc import ABC,abstractmethod
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.reader.IFengSchemaFactory import IFengSchemaFactory
from sele.spider.MultiMaterialSpider import MultiMaterialSpider    

class NAPS(ABC):
  '''
  1. Crawl a materail
  2. Login the publish page
  3. Publish
  4. Set published log
  '''

  def execute(self):
    self.spide()
    self.publish()
  
  @abstractmethod
  def publish(self):
    pass

  def spide(self):
    '''
    Crawl a material
    Return:
      {bool}
    '''
    factory = IFengSchemaFactory()
    tech_schema = factory.create_tech_news_schema()
    host_schema = factory.create_hot_news_schema()
    schemas = [tech_schema,host_schema]
    spider = MultiMaterialSpider(schemas)
    return spider.spide()
 



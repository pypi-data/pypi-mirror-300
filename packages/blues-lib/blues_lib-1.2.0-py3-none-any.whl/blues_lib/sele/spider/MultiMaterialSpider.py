from .MaterialSpider import MaterialSpider    

class MultiMaterialSpider(MaterialSpider):

  def __init__(self,schemas):
    self.schemas = schemas

  def spide(self):
    for schema in self.schemas:
      spider = MaterialSpider(schema)
      stat = spider.spide()
      if stat:
        break

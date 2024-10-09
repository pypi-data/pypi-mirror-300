import sys,re,os,json
from .MaterialReader  import MaterialReader  
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.browser.BluesStandardChrome import BluesStandardChrome
from pool.BluesMaterialIO import BluesMaterialIO
from util.BluesConsole import BluesConsole 

class MaterialSpider():

  def __init__(self,reader_schema):
    self.reader_schema = reader_schema 
    # the original authors, they should be replaced by the system author
    self.author_atom = reader_schema.author_atom
    self.image_size_atom = reader_schema.image_size_atom
    self.browser = BluesStandardChrome()
    self.system_author = '深蓝'

  def crawl(self):
    reader = MaterialReader(self.browser,self.reader_schema)
    rows = reader.read()
    return rows

  def spide(self):
    rows = self.crawl()
    stat = True
    if not rows:
      BluesConsole.error('No available materials')
      stat = False
    else:
      BluesConsole.success('Crawled %s materials' % str(len(rows)))
      result = self.__post(rows)
      if result['code'] == 200:
        BluesConsole.success('Inserted %s materials successfully' % result['count'])
        stat = True
      else:
        BluesConsole.error('Failed to insert, %s' % result.get('message'))
        stat = False

    self.browser.quit()
    return stat

  def __post(self,rows):
    entities = self.__get_entities(rows)
    return BluesMaterialIO.insert(entities)

  def __get_entities(self,rows):
    entities = []
    for row in rows:
      entity = self.__get_std_entity(row)
      if BluesMaterialIO.is_legal_material(entity):
        entities.append(entity)
    return entities

  def __get_std_entity(self,row):
    entity = {**row}
    # convert online image to local image
    entity['material_thumbnail'] = BluesMaterialIO.get_download_thumbnail(entity)
    
    # must download body image after the thumbnail downloaded
    self.__transfer_body(entity)
    
    body_dict = self.__get_body_dict(entity['material_body'])

    # append extend fields
    entity['material_type'] = 'article'
    entity['material_recommend_pub_channel'] = 'events'
    entity['material_body_text'] = json.dumps(body_dict['text'],ensure_ascii=False)
    entity['material_body_image'] = json.dumps(body_dict['image'],ensure_ascii=False)

    # convert the dict to json
    entity['material_body'] = json.dumps(entity['material_body'],ensure_ascii=False)
    return entity

  def __transfer_body(self,material):
    paras = material.get('material_body')
    material_thumbnail = material.get('material_thumbnail')
    image_count = 0
    for para in paras:
      # download and deal image
      if para['type'] == 'image':
        image_count += 1
        para['value'] = BluesMaterialIO.get_download_image(material,para['value'])
      elif para['type'] == 'text': 
        # replace the author
        para['value'] = self.__get_clean_text(para['value'])
    
    # make sure have at least one image
    if not image_count:
      paras.append({'type':'image','value':material_thumbnail})

  def __get_clean_text(self,text):
    # replace the author
    original_authors = self.author_atom.get_value()
    if not original_authors:
      return text

    clean_text = text
    for author in original_authors:
      clean_text = clean_text.replace(author,self.system_author)

    return clean_text

  def __get_body_dict(self,paras):
    body_dict = {
      'text':[],
      'image':[],
    }
    for para in paras:
      body_dict[para['type']].append(para['value'])
    
    # set the max image count
    max_image_size = self.image_size_atom.get_value()
    body_dict['image'] = body_dict['image'][:max_image_size]
    return body_dict





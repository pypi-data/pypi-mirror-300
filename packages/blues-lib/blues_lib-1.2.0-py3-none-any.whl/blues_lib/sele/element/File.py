import sys,os,re,time
from .deco.InfoKeyDeco import InfoKeyDeco
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.waiter.Querier import Querier  
from sele.element.Info import Info  
from pool.BluesFilePool import BluesFilePool
from util.BluesFiler import BluesFiler
from util.BluesDateTime import BluesDateTime

class File():

  def __init__(self,driver):
    self.__driver = driver
    self.__querier = Querier(driver,1) 
    self.__info = Info(driver) 

  def write(self,target_CS_WE,file,wait_time=5,parent_CS_WE=None):
    '''
    Add one or multiple files to the file input
    If there are multiple files, the upload mode is controlled based on whether multiple file upload is supported
    '''

    files = file if type(file) == list else [file]

    # Supports uploading multiple images at a time
    exist_files = BluesFiler.filter_exists(files)
    web_element = self.__querier.query(target_CS_WE,parent_CS_WE)
    if not exist_files or not web_element:
      return

    is_multiple = self.__info.get_attr(web_element,'multiple')
    if is_multiple:
      # must join the file paths by \n
      file_lines = '\n'.join(exist_files)
      web_element.send_keys(file_lines)
      BluesDateTime.count_down({'duration':wait_time,'title':'Wait image upload...'})
    else:
      for exist_file in exist_files:
        web_element.send_keys(exist_file)
        BluesDateTime.count_down({'duration':wait_time,'title':'Wait image upload...'})

  def download_image(self,image_CS_WE,image_dir=None,parent_CS_WE=None):
    '''
    Returns:
      {dict} : format download output, like:
        {'code':200,files:[],'message':''}
    '''
    image_CS_WEs = image_CS_WE if type(image_CS_WE)==list else [image_CS_WE]
    urls = self.get_img_urls(image_CS_WEs,parent_CS_WE)
    if urls:
      default_dir = BluesFilePool.get_dir_path(['download','img']) 
      file_dir = image_dir if image_dir else default_dir
      return BluesFiler.download(urls,file_dir)
    else:
      return None

  def get_img_urls(self,image_CS_WE,parent_CS_WE):
    '''
    Get all img urls from multiple selectors
    '''
    if not image_CS_WE:
      return None
    
    image_CS_WEs = image_CS_WE if type(image_CS_WE)==list else [image_CS_WE]

    urls = []
    for image_CS_WE in image_CS_WEs:
      if not image_CS_WE:
        continue
      current_urls = self.__get_img_urls(image_CS_WE,parent_CS_WE)
      if current_urls:
        urls.extend(current_urls)
    return urls

  def __get_img_urls(self,target_CS_WE,parent_CS_WE):
    '''
    Support img or other elements
    Returns:
      {list<str>} : the url list
    '''
    web_element = self.__querier.query(target_CS_WE,parent_CS_WE)
    if not web_element:
      return None
    urls = []
    if web_element.tag_name == 'img':
      url = self.__info.get_attr(web_element,'src')
      if url:
        urls.append(url)
    else:
      img_elements = self.__querier.query_all('img',web_element)
      if img_elements:
        for img_element in img_elements:
          url = self.__info.get_attr(img_element,'src')
          if url:
            urls.append(url)
    return urls


  # == module 2: element shot == #
  @InfoKeyDeco('screenshot')
  def screenshot(self,CS_WE,file):
    '''
    @description 指定元素截图,不支持base64格式
    @param {str} selector : css selector 
    @param {str} file 保存位置
    @returns {str} file_path
    '''
    file_path = file if file else self.__get_default_file()
    web_element = self.__querier.query(CS_WE)
    shot_status = web_element.screenshot(file_path)
    return file_path if shot_status else ''

  def __get_default_file(self,prefix='elementshot'):
    dir_path = BluesFilePool.get_dir_path('screenshot') 
    file_name = BluesFilePool.get_file_name(prefix=prefix,extension='png')
    return os.path.join(dir_path,file_name)

  

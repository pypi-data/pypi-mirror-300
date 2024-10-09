import sys,os,re,random,time
from selenium.webdriver.common.keys import Keys
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.waiter.Querier import Querier  

class Input():

  def __init__(self,driver):
    self.__driver = driver
    self.__querier = Querier(driver,1)

  def write(self,target_CS_WE,text,parent_CS_WE=None):
    '''
    Clear and write text into the text controller
    Parameter:
      target_CS_WE {str | WebElement} : the input element's css selecotr or web element
      texts {list<str>} : one or more text string
    '''
    web_element = self.__querier.query(target_CS_WE,parent_CS_WE)
    if not web_element:
      return None

    self.clear(web_element,None)
    self.append(web_element,text,None)

  def append(self,target_CS_WE,text,parent_CS_WE=None):
    '''
    Append text into the text controller
    Parameter:
      target_CS_WE {str | WebElement} : the input element's css selecotr or web element
      texts {list<str>} : one or more text string
    '''
    texts = text if type(text)==list else [text]

    web_element = self.__querier.query(target_CS_WE,parent_CS_WE)
    if not web_element:
      return None

    web_element.send_keys(*texts)

  def write_para(self,target_CS_WE,text,LF_count=1,parent_CS_WE=None):
    '''
    Write lines with line break
    Parameter:
      target_CS_WE {str | WebElement} : the input element's css selecotr or web element
      parent_CS_WE {str | WebElement} : the input element parent's css selecotr or web element
      texts {list<str>} : texts
      LF_count {int} : line break count in every para
    '''
    texts = text if type(text)==list else [text]
    paras = self.__get_paras(texts,LF_count)
    self.write(target_CS_WE,paras,parent_CS_WE)

  def append_para(self,target_CS_WE,text,LF_count=1,parent_CS_WE=None):
    texts = text if type(text)==list else [text]
    paras = self.__get_paras(texts,LF_count)
    self.append(target_CS_WE,paras,parent_CS_WE)

  def __get_paras(self,texts,LF_count):
    break_texts = []
    idx = 0
    max_idx = len(texts)-1
    for text in texts:
      break_texts.append(text)
      if idx<max_idx:
        for i in range(LF_count):
          break_texts.append(Keys.ENTER)
      idx+=1
    return break_texts

  def write_discontinuous(self,target_CS_WE,text,parent_CS_WE=None):
    web_element = self.__querier.query(target_CS_WE,parent_CS_WE)
    if not web_element:
      return None

    self.clear(web_element,None)
    self.append_discontinuous(web_element,text,None)
  
  def append_discontinuous(self,target_CS_WE,text,parent_CS_WE=None):
    '''
    Input chars non-uniform speed
    '''
    texts = text if type(text)==list else [text]
    web_element = self.__querier.query(target_CS_WE,parent_CS_WE)

    for text in texts:
      # input char by char
      for char in text:
        self.__input_discontinuous(web_element,char)

  def __input_discontinuous(self,web_element,char,min=0.2,max=1.5):
    '''
    input the text one char by one char intermittently
    using a random interval
    '''
    interval = round(random.uniform(min,max),1)
    time.sleep(interval)
    web_element.send_keys(char)

  def clear(self,target_CS_WE,parent_CS_WE=None):
    web_element = self.__querier.query(target_CS_WE,parent_CS_WE)
    web_element.clear()

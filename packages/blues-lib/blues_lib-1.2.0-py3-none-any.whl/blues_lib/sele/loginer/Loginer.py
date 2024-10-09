import sys,os,re
from abc import ABC, abstractmethod
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.browser.BluesProxyChrome import BluesProxyChrome     
from util.BluesURL import BluesURL      
from util.BluesDateTime import BluesDateTime        
from util.BluesConsole import BluesConsole        

class Loginer(ABC):

  def __init__(self):

    # { LoginerSchema } 
    self.loginer_schema = None
    
    # { LoginerBrowser }
    self.browser = None
    
    self.prepare_loginer_schema()
    self.prepare()
    self.prepare_perform_atom()

  def prepare(self):
    '''
    Split the loginer schema to class attributes
    '''
    # { str } the login page url
    self.url = self.loginer_schema.url_atom.get_value()
    # { str } the element of login page 
    self.mark = self.loginer_schema.mark_atom.get_value()
    # { int } the page load timeout
    self.timeout = self.loginer_schema.timeout_atom.get_value()
    # { dict } the proxy's config
    self.proxy_config = self.loginer_schema.proxy_atom.get_value()
    # { dict } the cookies filter config
    self.cookie_filter_config = self.loginer_schema.cookie_filter_atom.get_value()

  @abstractmethod
  def perform(self):
    '''
    Perform switch, fill, submit
    '''
    pass

  @abstractmethod
  def prepare_loginer_schema(self):
    pass

  @abstractmethod
  def prepare_perform_atom(self):
    pass

  def login(self):
    '''
    @description : final method
    '''
    try:
      self.open()
      self.perform()
      self.verify()
      self.save_cookies()
    except Exception as e:
      BluesConsole.error('Login failure: %s' % e)
    finally:
      self.quit()
  
  def open(self):
    proxy_config = self.proxy_config if self.proxy_config else self.get_default_proxy_config()
    self.browser = BluesProxyChrome(proxy_config,self.cookie_filter_config)
    self.browser.open(self.url)

  def get_default_proxy_config(self):
    main_domain = BluesURL.get_main_domain(self.url)
    scopes = [".*%s.*" % main_domain]
    return {
      "scopes":scopes,
    }

  def verify(self):
    BluesDateTime.count_down({
      'title':'Wait for login and jump',
      'duration':self.timeout
    })

    if self.browser.element.finder.find(self.mark):
      raise Exception('Login failure')
    
    BluesConsole.success('Login successfully, ready to save cookies')

  def save_cookies(self):
    cookie_file = self.browser.save_cookies()
    if cookie_file:
      BluesConsole.success('The cookie has been successfully obtained and saved')
    else:
      BluesConsole.success('Cookie acquisition failure')

  def quit(self):
    if self.browser:
      self.browser.quit()

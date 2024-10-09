import sys,os,re
from abc import ABC, abstractmethod

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.browser.BluesProxyChrome import BluesProxyChrome     
from util.BluesURL import BluesURL      
from util.BluesConsole import BluesConsole       
from util.BluesDateTime import BluesDateTime        
from sele.publisher.writer.FormWriter import FormWriter

class BluesLoginer(ABC):
  '''
  The superclass of login to define all tmeplate methods
  '''

  def __init__(self,loginer_schema,loginer_config):
    '''
    Parameter:
      loginer_schema {BluesLoginerSchema} : the login form and host meta
      loginer_config {dict<str,dict>} : the proxy and cookie config
    '''
    self.__loginer_schema = loginer_schema
    self.__loginer_config = loginer_config
    
    # Avoid starting the browser too early, assign this attribute in execute method
    self.__browser = None

    self.__prepare()

  def __prepare(self):
    self.__opener_schema = self.__loginer_schema.get_opener_schema()
    self.__former_schema = self.__loginer_schema.get_former_schema()
    
    # destruct opener attrs
    self.__page_url = self.__opener_schema.gain_page_url()
    self.__page_selector = self.__opener_schema.gain_page_selector()
    self.__load_timeout = self.__opener_schema.gain_load_timeout()

    # destruct former atters
    self.__form_atoms = self.__former_schema.get_form_atoms()
    self.__host_atoms = self.__former_schema.get_host_atoms()
    
    # scope and cookie pattern are regexp strings
    self.__proxy_config = self.__loginer_config.get('proxy',self.__get_default_proxy_config())
    self.__cookie_config = self.__loginer_config.get('cookie')

  def execute(self):
    '''
    @description : final method
    '''
    self.__set_browser()
    self.__open_page()
    self.__perform_host_action() 
    self.__perform_form_action() 
    stat = self.__is_login()
    if not stat:
      BluesConsole.error('Login failure')
      return

    BluesConsole.success('Login successfully, ready to save cookies')
    self.__save_cookies()
    self.__quit()

  def __set_browser(self):
    self.__browser = BluesProxyChrome(self.__proxy_config,self.__cookie_config)

  def __get_default_proxy_config(self):
    main_domain = BluesURL.get_main_domain(self.__page_url)
    scopes = [".*%s.*" % main_domain]
    return {
      "scopes":scopes,
    }

  def __open_page(self):
    self.__browser.get(self.__page_url)

  def __perform_host_action(self):
    if self.__host_atoms:
      # Wait to be implemented
      pass

  def __perform_form_action(self):
    writer = FormWriter(self.__browser,self.__form_atoms)
    writer.write()

  def __save_cookies(self):
    cookie_file = self.__browser.save_cookies()
    if cookie_file:
      BluesConsole.success('The cookie has been successfully obtained and saved')
    else:
      BluesConsole.success('Cookie acquisition failure')

  def __is_login(self):
    '''
    Check whether the login is complete. 
    If you are still on the login page after 15 seconds, the login fails
    Check the login page elements to reduce entries
    
    Returns:
      {bool}
    '''
    BluesDateTime.count_down({
      'title':'Waiting to verify the login status',
      'duration':self.__load_timeout
    })

    if self.__browser.action.element.find(self.__page_selector):
      return False 
    else:
      return True
  
  def __quit(self):
    self.__browser.quit()


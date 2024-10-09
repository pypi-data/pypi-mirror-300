import sys,os,re
from .BluesCookie import BluesCookie    
from .BluesStandardChrome import BluesStandardChrome   

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesConsole import BluesConsole   
from util.BluesPowerShell import BluesPowerShell    
from util.BluesType import BluesType    
#from sele.login.BluesLoginerFactory import BluesLoginerFactory      

class BluesLoginChrome(BluesStandardChrome,BluesCookie):
  '''
  This class is used exclusively to open pages that can only be accessed after login
  There are three ways to complete automatic login:
    1. Login by a cookie string
    2. Login by a cookie file path
    3. Login by the BluesLoginer class
  '''
  
  # Maximum relogin times
  max_relogin_time = 1

  def __init__(self,opener_schema,loginer=None):
    '''
    Parameter:
      opener_schema (BluesOpenerSchema) : Open the page with the passed or local cookies
      loginer (BluesLoginerSchema) : If the local cookies don't work, relogin and save the cookies
    '''
    super().__init__()
    
    # current relogin times
    self.relogin_time = 0
    self.opener_schema = opener_schema
    self.loginer = loginer

    # destruct the atom's value 
    self.__prepare()

    # open the page
    self.__open()

  def __prepare(self):
    self.url = self.opener_schema['url_atom'].get_value()
    self.mark = self.opener_schema['mark_atom'].get_selector()
    self.cookie_value = None #self.opener_schema.get_cookie_value()
    self.cookie_file = None #self.opener_schema.get_cookie_file()

  def __open(self):

    # Open a page and determine whether to jump to the login page
    self.open(self.url)
    if self.__is_login():
      BluesConsole.info('You are currently logged in')
      return

    # Get the cookie from input parameter or local file
    cookies = self.__get_cookies()
    if not cookies:
      BluesConsole.info('Local cookie is missing, log in aget')
      # Scenario 1: has no existed cookies
      self.__relogin()
      return

    # Reopen the page with the local cookies
    BluesConsole.info('Try logging in with local cookies: %s' % cookies)
    self.interactor.cookie.set(cookies) 
    self.open(self.url)
    if self.__is_login():
      BluesConsole.success('Login successfully')
      return 

    # Relogin
    BluesConsole.info('The local cookie has expired, log in aget')
    self.__relogin()
    
  def __get_cookies(self):
    if self.cookie_value:
      return self.cookie_value

    return self.read_cookies(self.cookie_file,self.driver.current_url)

  def __is_login(self):
    '''
    Whether the page opened correctly 
    Parameter:
      wait_time {int} : Waiting time (ms)
    @return:
      {bool} : If you are not logged in, you are redirected to the login page
    '''
    if self.waiter.querier.query(self.mark):
      return True 
    else:
      return False
  
  def __relogin(self):
    if not self.loginer:
      BluesConsole.error('Login failed, the loginer parameter is missing')
      return

    if self.relogin_time>=self.max_relogin_time:
      BluesConsole.error('Login failed, the maximum number of relogins has been reached.')
      return

    self.relogin_time+=1
    
    # Relogin and save the new cookies to the local file
    BluesConsole.info('Relogin using the %s' % type(self.loginer).__name__)
    self.loginer.login()
    
    # Refresh the page to get the new token in the document before reopen
    self.interactor.navi.refresh() 

    # Reopen the page using the new cookies
    self.__open()

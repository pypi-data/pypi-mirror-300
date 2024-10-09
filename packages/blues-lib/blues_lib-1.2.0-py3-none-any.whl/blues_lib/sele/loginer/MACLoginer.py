import sys,os,re,time
from datetime import datetime
from .Loginer import Loginer 

sys.path.append(re.sub('src.*','src',os.getcwd()))
#from service.controller.UserPostController import UserPostController  

class MACLoginer(Loginer):

  def __init__(self,*args):
    super().__init__(*args)

  def fill_and_submit(self):

    self.form_action.text('phone',self.account['phone'])

    # Slide verification if the slider is present
    self.form_action.slide('slider')

    # send sms code
    self.form_action.click('send')
    # send sms notification

    time = datetime.now()
    self.mailer.send_mac_notification(self.meta['platform'],self.account['phone'],time)
    
    response = self.get_code(time)
    # 查询验证码
    if response.code==200:
      code = response.data[0]['up_value']

      if not code:
        print('===> Error: Get a empty code')
        return

      # 写入验证码
      self.form_action.text('code',code)

      self.form_action.click('submit')

    else:
      print('===> Error: The user timed out and did not log in (%s)' % response.message)

  
  def get_code(self,time):
    timestamp = str(int(time.timestamp()*1000))
    #upc = UserPostController()
    condition = {
      'up_mode':'mac',
      'up_user':self.account['phone'],
      'up_platform':self.meta['platform'],
      'up_timestamp':timestamp,
    }
    return upc.wait_user_post(condition,300,10)

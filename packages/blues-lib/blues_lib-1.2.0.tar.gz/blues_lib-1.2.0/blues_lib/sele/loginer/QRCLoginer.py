import sys,os,re,time
from datetime import datetime
from .parent.Login import Login 

sys.path.append(re.sub('src.*','src',os.getcwd()))
from service.controller.UserPostController import UserPostController  

class QRCLogin(Login):

  def __init__(self,*args):
    super().__init__(*args)

  def fill_and_submit(self):
    file_name = self.meta['platform']+'_'+self.account['name']
    base64= self.file_action.element_shot('qrcode',file_name)

    time = datetime.now()
    self.mailer.send_qrc_notification(self.meta['platform'],self.account['name'],time,base64)

    response = self.get_code(time)
    # 查询验证码
    if response.code==200:
      code = response.data[0]['up_value']

      # The afterLoginHook will check whether the login is indeed successful
      if code !='200': # as string
        print('===> Error: User log in failure')
        return

    else:
      print('===> Error: The user timed out and did not log in (%s)' % response.message)


  def get_code(self,time):
    timestamp = str(int(time.timestamp()*1000))
    upc = UserPostController()
    condition = {
      'up_mode':'qrc',
      'up_user':self.account['name'],
      'up_platform':self.meta['platform'],
      'up_timestamp':timestamp,
    }
    return upc.wait_user_post(condition,300,10)

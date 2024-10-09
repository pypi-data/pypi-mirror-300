from .BaiJiaAccountLoginer import BaiJiaAccountLoginer   
from .BaiJiaMACLoginer import BaiJiaMACLoginer   

class BaiJiaLoginerFactory():

  def create_account_loginer(self):
    return BaiJiaAccountLoginer()

  def create_mac_loginer(self):
    return BaiJiaMACLoginer()

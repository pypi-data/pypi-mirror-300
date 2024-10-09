from .TouTiaoAccountLoginer import TouTiaoAccountLoginer   
from .TouTiaoMACLoginer import TouTiaoMACLoginer   

class BluesLoginerFactory():

  def create_account_loginer(self):
    return TouTiaoAccountLoginer()

  def create_mac_loginer(self):
    return TouTiaoMACLoginer()

from .LoginerSchemaFactory import LoginerSchemaFactory
from .BaiJiaAccountLoginerSchema import BaiJiaAccountLoginerSchema
from .BaiJiaMACLoginerSchema import BaiJiaMACLoginerSchema

class BaiJiaLoginerSchemaFactory(LoginerSchemaFactory):

  def create_account_schema(self):
    return BaiJiaAccountLoginerSchema()

  def create_mac_schema(self):
    return BaiJiaMACLoginerSchema()

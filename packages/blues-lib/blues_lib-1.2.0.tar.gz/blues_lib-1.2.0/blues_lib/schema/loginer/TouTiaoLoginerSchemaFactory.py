from .LoginerSchemaFactory import LoginerSchemaFactory
from .TouTiaoAccountLoginerSchema import TouTiaoAccountLoginerSchema
from .TouTiaoMACLoginerSchema import TouTiaoMACLoginerSchema

class TouTiaoLoginerSchemaFactory(LoginerSchemaFactory):

  def create_account_schema(self):
    return TouTiaoAccountLoginerSchema()

  def create_mac_schema(self):
    return TouTiaoMACLoginerSchema()

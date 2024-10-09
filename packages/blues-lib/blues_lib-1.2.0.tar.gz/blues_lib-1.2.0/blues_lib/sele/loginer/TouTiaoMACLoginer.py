import sys,os,re
from MACLoginer import MACLoginer

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.TouTiaoLoginerSchemaFactory import TouTiaoLoginerSchemaFactory

class TouTiaoMACLoginer(MACLoginer):

  def prepare_loginer_schema(self):
    factory = TouTiaoLoginerSchemaFactory()
    self.loginer_schema = factory.create_mac_schema()

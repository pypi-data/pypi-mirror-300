import sys,os,re
from AccountLoginer import AccountLoginer

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.TouTiaoLoginerSchemaFactory import TouTiaoLoginerSchemaFactory

class TouTiaoAccountLoginer(AccountLoginer):

  def prepare_loginer_schema(self):
    factory = TouTiaoLoginerSchemaFactory()
    self.loginer_schema = factory.create_account_schema()

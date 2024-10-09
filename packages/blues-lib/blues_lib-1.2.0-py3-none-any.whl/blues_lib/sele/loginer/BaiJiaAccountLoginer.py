import sys,os,re
from .AccountLoginer import AccountLoginer

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.BaiJiaLoginerSchemaFactory import BaiJiaLoginerSchemaFactory

class BaiJiaAccountLoginer(AccountLoginer):

  def prepare_loginer_schema(self):
    factory = BaiJiaLoginerSchemaFactory()
    self.loginer_schema = factory.create_account_schema()

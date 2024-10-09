import sys,os,re

from .NAPS import NAPS
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.releaser.BaiJiaReleaserSchemaFactory import BaiJiaReleaserSchemaFactory
from sele.loginer.BaiJiaLoginerFactory import BaiJiaLoginerFactory   
from sele.publisher.Publisher import Publisher

class BaiJiaEventsNAPS(NAPS):
  '''
  1. Crawl a materail
  2. Login the publish page
  3. Publish
  4. Set published log
  '''

  def publish(self):
    releaser_schema = self.get_releaser_schema()
    loginer = self.get_loginer()

    publisher = Publisher(releaser_schema,loginer)
    publisher.publish()

  def get_releaser_schema(self):
    factory = BaiJiaReleaserSchemaFactory()
    return factory.create_events_schema()

  def get_loginer(self):
    loginer_factory = BaiJiaLoginerFactory()
    return loginer_factory.create_account_loginer()


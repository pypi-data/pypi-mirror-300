from .ReleaserSchemaFactory import ReleaserSchemaFactory
from .BaiJiaEventsReleaserSchema import BaiJiaEventsReleaserSchema
from .BaiJiaNewsReleaserSchema import BaiJiaNewsReleaserSchema

class BaiJiaReleaserSchemaFactory(ReleaserSchemaFactory):

  def create_events_schema(self):
    return BaiJiaEventsReleaserSchema()

  def create_news_schema(self):
    return BaiJiaNewsReleaserSchema()

from .ReleaserSchemaFactory import ReleaserSchemaFactory
from .TouTiaoEventsReleaserSchema import TouTiaoEventsReleaserSchema
from .TouTiaoNewsReleaserSchema import TouTiaoNewsReleaserSchema

class TouTiaoReleaserSchemaFactory(ReleaserSchemaFactory):

  def create_events_schema(self):
    return TouTiaoEventsReleaserSchema()

  def create_news_schema(self):
    return TouTiaoNewsReleaserSchema()

from .ReaderSchemaFactory import ReaderSchemaFactory
from .IFengTechNewsSchema import IFengTechNewsSchema
from .IFengHotNewsSchema import IFengHotNewsSchema
from .IFengGalleryReaderSchema import IFengGalleryReaderSchema

class IFengSchemaFactory(ReaderSchemaFactory):

  def create_tech_news_schema(self):
    return IFengTechNewsSchema()

  def create_hot_news_schema(self):
    return IFengHotNewsSchema()

  def create_gallery_schema(self):
    return IFengGalleryReaderSchema()

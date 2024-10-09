from .ReaderSchemaFactory import ReaderSchemaFactory
from .BBCNewsReaderSchema import BBCNewsReaderSchema
from .BBCGalleryReaderSchema import BBCGalleryReaderSchema

class BBCReaderSchemaFactory(ReaderSchemaFactory):

  def create_news_schema(self):
    return BBCNewsReaderSchema()

  def create_gallery_schema(self):
    return BBCGalleryReaderSchema()


# plain atoms
from .plain.DataAtom import DataAtom
from .plain.RegexpAtom import RegexpAtom
from .plain.URLAtom import URLAtom

# event atoms
from .event.ElementAtom import ElementAtom
from .event.ClickableAtom import ClickableAtom
from .event.FrameAtom import FrameAtom
from .event.RollinAtom import RollinAtom
from .event.PopupAtom import PopupAtom

# writer atoms
from .writer.InputAtom import InputAtom
from .writer.TextAreaAtom import TextAreaAtom
from .writer.FileAtom import FileAtom
from .writer.ChoiceAtom import ChoiceAtom
from .writer.SelectAtom import SelectAtom

# reader atoms
from .reader.AttrAtom import AttrAtom
from .reader.TextAtom import TextAtom
from .reader.ValueAtom import ValueAtom
from .reader.CssAtom import CssAtom

# composite
from .composite.ArrayAtom import ArrayAtom
from .composite.MapAtom import MapAtom

# spider atoms
from .spider.BriefAtom import BriefAtom
from .spider.NewsAtom import NewsAtom
from .spider.ParaAtom import ParaAtom

class AtomFactory():

  # create plain Atoms
  def createData(self,title,value):
    return DataAtom(title,value)

  def createRegexp(self,title,value):
    return RegexpAtom(title,value)

  def createURL(self,title,value):
    return URLAtom(title,value)

  # create event Atoms
  def createElement(self,title,selector,value=None):
    return ElementAtom(title,selector,value)

  def createRollin(self,title,selector,value=None):
    return RollinAtom(title,selector,value)

  def createPopup(self,title,selector,value=None):
    return PopupAtom(title,selector,value)

  def createClickable(self,title,selector,value=None):
    return ClickableAtom(title,selector,value)

  def createFrame(self,title,selector,value=None):
    return FrameAtom(title,selector,value)
  
  # create writer Atoms
  def createInput(self,title,selector,value=None):
    return InputAtom(title,selector,value)

  def createTextArea(self,title,selector,value=None,LF_count=1):
    return TextAreaAtom(title,selector,value,LF_count)

  def createFile(self,title,selector,value=None,wait_time=2):
    return FileAtom(title,selector,value)

  def createSelect(self,title,selector,value=True):
    return SelectAtom(title,selector,value)

  def createChoice(self,title,selector,value=True):
    return ChoiceAtom(title,selector,value)

  # reader atoms
  def createText(self,title,selector,value=None,parent_selector=None):
    return TextAtom(title,selector,value,parent_selector)

  def createValue(self,title,selector,value=None,parent_selector=None):
    return ValueAtom(title,selector,value,parent_selector)

  def createAttr(self,title,selector,value=None,parent_selector=None):
    return AttrAtom(title,selector,value,parent_selector)

  def createCss(self,title,selector,value=None,parent_selector=None):
    return CssAtom(title,selector,value,parent_selector)
  
  # composite atoms
  def createArray(self,title,value=None):
    return ArrayAtom(title,value)

  def createMap(self,title,value=None):
    return MapAtom(title,value)

  # spider atoms
  def createPara(self,title,selector,value):
    return ParaAtom(title,selector,value)

  def createBrief(self,title,selector,value):
    return BriefAtom(title,selector,value)

  def createNews(self,title,selector,value):
    return NewsAtom(title,selector,value)

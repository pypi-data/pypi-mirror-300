from .ReaderAtom import ReaderAtom

class CssAtom(ReaderAtom):

  _kind = 'css' 

  def __init__(self,title,selector,value,config={}):
    '''
    A common element
    Parameter:
      title (str) : the atom's description
      selector (str) : the elemetn css selector
      value (str) : the value
      config (dict) : the reader's settings
    Returns:
      BluesAtom : a atom instance
    '''
    super().__init__(self._kind,title,selector,value,config)


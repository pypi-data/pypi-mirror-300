from .EventAtom import EventAtom

class FrameAtom(EventAtom):
    
  kind = 'frame'

  def __init__(self,title,selector,value=None):
    '''
    A iframe element atom
    Parameter:
      title (str) : the atom's title
      selector (str) : the element's css selector
      value (any) : the optional value, base on the atom's kind
    Returns:
      Atom : a atom instance
    '''
    super().__init__(self.kind,title,selector,value)



from .WriterAtom import WriterAtom

class FileAtom(WriterAtom):

  _kind = 'file' 

  def __init__(self,title,selector,value,wait_time=5):
    '''
    A file type input element
    Parameter:
      title (str) : the atom's description
      selector (str) : the text input's css selector
      value (str|list) : the file or file list
    Returns:
      BluesAtom : a atom instance
    '''
    super().__init__(self._kind,title,selector,value)
    self._wait_time = wait_time

  # getter
  def get_wait_time(self):
    return self._wait_time
  
  # setter
  def set_wait_time(self,wait_time):
    self._wait_time = wait_time
 

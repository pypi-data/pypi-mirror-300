import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.behavior.Behavior import Behavior
from sele.behavior.deco.BehaviorDeco import BehaviorDeco
from entity.STDOut import STDOut

class Rollin(Behavior):

  @BehaviorDeco()
  def resolve(self):
    '''
    Just move the element into the window
    '''
    if self.kind!='rollin':
      return False 
    
    self.browser.action.wheel.scroll_from_element_to_offset(self.selector,0,50)
    return STDOut()

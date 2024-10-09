import sys,os,re
from .Loginer import Loginer
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.behavior.BehaviorChain import BehaviorChain

class AccountLoginer(Loginer):

  def prepare_perform_atom(self):
    # { MacroAtom } the switch atom list
    self.switch_atom = self.loginer_schema.switch_atom    
    # { MacroAtom } the fill atom list
    self.fill_atom = self.loginer_schema.fill_atom    
    # { MacroAtom } the submit atom list
    self.submit_atom = self.loginer_schema.submit_atom    
    
  def perform(self):
    self.switch() 
    self.fill() 
    self.submit() 
  
  def switch(self):
    handler = BehaviorChain(self.browser,self.switch_atom)
    handler.handle()

  def fill(self):
    handler = BehaviorChain(self.browser,self.fill_atom)
    handler.handle()

  def submit(self):
    handler = BehaviorChain(self.browser,self.submit_atom)
    handler.handle()

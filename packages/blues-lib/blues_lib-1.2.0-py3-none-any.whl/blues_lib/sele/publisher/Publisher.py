import sys,os,re,time
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.browser.BluesLoginChrome import BluesLoginChrome    
from sele.behavior.FormBehavior import FormBehavior       
from pool.BluesMaterialIO import BluesMaterialIO
from report.MaterialReport import MaterialReport
from util.BluesDateTime import BluesDateTime
from util.BluesConsole import BluesConsole

class Publisher():

  def __init__(self,releaser_schema,loginer=None):
    self.releaser_schema = releaser_schema
    self.loginer = loginer

    self.material = releaser_schema.material
    self.browser = None
    # publish status: 'available','published','pubsuccess','pubfailure','illegal'
  
  def publish(self):
    '''
    @description : the final method
    '''
    if not self.material:
      BluesConsole.error('No available materials')
      return

    try:
      # step1: crawl material
      # step2: login 
      self.open()
      self.fill()
      self.verify_before_submit()
      self.preview()
      self.submit()
      self.verify_after_submit()

    except Exception as e:
      self.material['material_status'] = 'pubfailure'
      BluesConsole.error(e,'Publish failure')
    finally:
      self.clean()
      self.record()
      self.quit()

  def test(self):
    self.material['material_status'] = 'pubsuccess'
    self.open()
    self.clean()
    self.record()
    self.quit()
      
  def open(self):
    # temp structure
    opener_schema = {
      'url_atom' : self.releaser_schema.url_atom,
      'mark_atom' : self.releaser_schema.mark_atom
    }
    self.browser = BluesLoginChrome(opener_schema,self.loginer)
    BluesConsole.success('Opened form page: %s' % self.browser.interactor.document.get_title())

  def quit(self):
    if self.browser:
      self.browser.quit()

  def fill(self):
    '''
    @description : override by the concrete publisher
    '''
    fill_atom = self.releaser_schema.fill_atom
    popup_atom = self.releaser_schema.popup_atom
    handler = FormBehavior(self.browser,fill_atom,popup_atom)
    handler.handle()
    BluesConsole.info('Form filled')

  def verify_before_submit(self):
    '''
    Verify is all required fields filled
    Use the fill_atom to verify
    '''
    BluesConsole.info('Form filled successfully')

  def preview(self):
    '''
    @description : preview before submit
    '''
    preview_atom = self.releaser_schema.preview_atom
    popup_atom = self.releaser_schema.popup_atom
    if preview_atom:
      handler = FormBehavior(self.browser,preview_atom,popup_atom)
      handler.handle()
      BluesConsole.info('Preview successfully')

  def submit(self):
    '''
    @description : submit
    '''
    submit_atom = self.releaser_schema.submit_atom
    popup_atom = self.releaser_schema.popup_atom
    if submit_atom:
      handler = FormBehavior(self.browser,submit_atom,popup_atom)
      handler.handle()
      BluesConsole.info('Submited successfully')

  def verify_after_submit(self):
    '''
    Verify whether the publication is successful.
    If the publication is successful and the page jumps, then the publishing button element will not exist.
    '''
    BluesDateTime.count_down({'duration':5,'title':'Verify submission status'})
    # Use the form page's submit element to make sure weather published succesfully
    submit_atom = self.releaser_schema.submit_atom
    first_ele = submit_atom.get_value()[0].get_selector()
    if not first_ele:
      self.material['material_status'] = 'published'
      BluesConsole.error('Published but does not verify the status')
      return

    stat = self.browser.element.state.is_presence(first_ele)
    if stat:
      self.material['material_status'] = 'pubfailure'
      BluesConsole.error('Published failure')
    else:
      self.material['material_status'] = 'pubsuccess'
      BluesConsole.success('Published successfully.')

  def clean(self):
    '''
    Update the meterial's status
    '''
    material_id = self.material.get('material_id')
    entity = {'material_status':self.material['material_status']}      
    conditions = [
      {'field':'material_id','comparator':'=','value':material_id}
    ]
    response = BluesMaterialIO.update(entity,conditions)
    if response.get('code') == 200 and response.get('count') == 1:
      BluesConsole.success('Updated the material status to [%s] successfully' % self.material['material_status'])
    else:
      BluesConsole.error('Updated the material status to [%s] failure, error: %s' % (self.material['material_status'],response.get('message')))


  def record(self):
    report = MaterialReport(self.browser,self.material)
    report.execute()
    



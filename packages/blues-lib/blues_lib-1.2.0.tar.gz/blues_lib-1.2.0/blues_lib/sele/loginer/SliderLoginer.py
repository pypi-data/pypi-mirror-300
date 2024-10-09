from .Login import Login 

class SliderLogin(Login):

  def __init__(self,*args):
    super().__init__(*args)

  def fill_and_submit(self):

    name = self.form_meta['name']
    self.browser.action.form.write(name,self.account['name'])

    password = self.form_meta['password']
    self.browser.action.form.write(password,self.account['password'])

    slider = self.form_meta['slider']
    container = slider['container']
    block = slider['block']
    self.browser.action.mover.slide(container,block,direction='right')

    submit = self.form_meta['submit']
    self.browser.action.event.click(submit)

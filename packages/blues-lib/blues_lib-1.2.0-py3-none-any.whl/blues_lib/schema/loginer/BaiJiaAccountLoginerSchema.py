from .AccountLoginerSchema import AccountLoginerSchema

class BaiJiaAccountLoginerSchema(AccountLoginerSchema):

  def get_url_atom(self):
    return self.atom_factory.createURL('Page URL','https://baijiahao.baidu.com/builder/theme/bjh/login')

  def get_mark_atom(self):
    return self.atom_factory.createElement('Login mark selector','div[class^=btnlogin]')

  def get_proxy_atom(self):
    config = {
      'scopes': ['.*baijiahao.baidu.com.*'],
    }
    return self.atom_factory.createData('proxy config',config)

  def get_cookie_filter_atom(self):
    config = {
      'url_pattern':'/builder/rc/home',
      'value_pattern':None
    }
    return self.atom_factory.createData('cookie filter config',config)
  
  def get_switch_atom(self):
    atom = [
      self.atom_factory.createClickable('switch to account mode','div[class^=btnlogin]'),
    ]
    return self.atom_factory.createArray('switch atom',atom)

  def get_fill_atom(self):
    atom = [
      self.atom_factory.createInput('name','#pass-login-main input[name=userName]','17607614755'),
      self.atom_factory.createInput('password','#pass-login-main input[name=password]','Langcai10.'),
      self.atom_factory.createChoice('agree protocal','#pass-login-main input[name=isAgree]',True),
      self.atom_factory.createChoice('remember me','#pass-login-main input[name=memberPass]',True),
    ]
    return self.atom_factory.createArray('fill atom',atom)

  def get_submit_atom(self):
    atom = [
      self.atom_factory.createClickable('submit','#pass-login-main input[type=submit]'),
    ]
    return self.atom_factory.createArray('submit atom',atom)


import sys,os,re,json
from .EventsReleaserSchema import EventsReleaserSchema

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from pool.BluesMaterialIO import BluesMaterialIO


class BaiJiaEventsReleaserSchema(EventsReleaserSchema):

  def set_material(self):
    response = BluesMaterialIO.latest()
    if not response.get('code')==200 or not response.get('data'):
      self.fill_atom = None
      return

    material = response.get('data')[0]

    title = material.get('material_title')
    texts = json.loads(material.get('material_body_text'))
    # append the title as the first line
    texts.insert(0,title)
    images = json.loads(material.get('material_body_image'))

    fill_dict = {
      'material_body_text':texts,
      'material_body_image':images
    }
    self.set_fill_value(fill_dict)
    self.material = material

  def get_url_atom(self):
    return self.atom_factory.createURL('events page','https://baijiahao.baidu.com/builder/rc/edit?type=events')

  def get_mark_atom(self):
    return self.atom_factory.createElement('form page mark','#content')

  def get_fill_atom(self):

    # use the filed plachehoders
    image_atom = [
      self.atom_factory.createClickable('Popup the dialog','.uploader-plus'),
      # value placeholder 1: material_body_image ,set wait_time as 5
      self.atom_factory.createFile('Select images','.cheetah-upload input','material_body_image',5),
      self.atom_factory.createClickable('Upload images','.cheetah-modal-footer button.cheetah-btn-primary'),
    ]

    atoms = [
      # value placeholder 2: material_body_text
      self.atom_factory.createTextArea('content','#content','material_body_text',2),
      self.atom_factory.createArray('images',image_atom),
    ]

    return self.atom_factory.createArray('fields',atoms)

  def get_preview_atom(self):
    return None

  def get_submit_atom(self):
    atoms = [
      self.atom_factory.createClickable('submit','.cheetah-public .events-op-bar-pub-btn'),
    ]
    return self.atom_factory.createArray('submit',atoms)

  def get_popup_atom(self):
    return None


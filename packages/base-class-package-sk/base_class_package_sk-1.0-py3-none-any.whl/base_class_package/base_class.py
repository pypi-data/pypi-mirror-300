class base:

  def __init__(self, value):
    self.value = value

  def get_value(self):
    return self.value

  def set_value(self, new_value):
    self.value = new_value

  def add_increment(self, incremenet):
    self.value += incremenet

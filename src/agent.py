global_id = 0

class Agent:
  def __init__(self):
    global global_id
    self.id = global_id
    global_id += 1

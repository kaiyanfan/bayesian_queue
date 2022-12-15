from enum import Enum

global_id = 0

"""
How does the agent select a queue
SHORTEST    ---  Pick the shortest queue
LEAST_LOAD  ---  Pick the queue with the least load
"""
class SelectionCriteria(Enum):
  SHORTEST = 0
  LEAST_LOAD = 1
  INFER = 2
  
class Agent:

  def __init__(self, arrivalTime, select_how=SelectionCriteria.SHORTEST):
    global global_id
    self.id = global_id
    global_id += 1
    
    self.arrivalTime = arrivalTime
    self.select_how = select_how
    self.quit_time = 100
    self.trials = 2
    self.been_served = False

  def select_shortest(self, queues):
    shortest, shortestLen = 0, queues[0].size()
    for i, q in enumerate(queues):
      if q.size() < shortestLen:
        shortest, shortestLen = i, q.size()
    return shortest
  
  def select_least_load(self, queues):
    least, least_load = 0, queues[0].load
    for i, q in enumerate(queues):
      if q.load < least_load:
        least, least_load = i, q.load
    return least

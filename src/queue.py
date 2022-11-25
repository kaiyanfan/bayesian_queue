import numpy as np

from event import Event, EventType

class Queue:
  def __init__(self, queueId, departMu):
    self.id = queueId
    self.queue = []
    self.mu = departMu
    self.numArrival = 0
    self.numDepart = 0
  
  """
  Calculate the time for the next departure time
  """
  def __scheduleTime(self, currTime):
    # service time is an exponential distibution
    return currTime + np.random.exponential(self.mu)

  """
  The arrival routine. Returns (optional) scheduled depart event
  """
  def arrive(self, agent, currTime):
    self.queue.append(agent)
    self.numArrival += 1
    # schedule the departure event if the queue was empty
    if len(self.queue) == 1:
      departTime = self.__scheduleTime(currTime)
      event = Event(self.id, EventType.DEPART, departTime)
      return event
    return None

  """
  The departure routine. Returns (optional) scheduled depart event
  """
  def depart(self, currTime):
    print(f"Agent {self.queue[0].id} departs queue {self.id} at {currTime}")
    self.queue = self.queue[1:]
    self.numDepart += 1
    # schedule the departure event if the queue isn't empty
    if len(self.queue) > 0:
      departTime = self.__scheduleTime(currTime)
      event = Event(self.id, EventType.DEPART, departTime)
      return event
    return None

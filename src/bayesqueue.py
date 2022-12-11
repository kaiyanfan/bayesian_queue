import numpy as np

from event import Event, EventType

class Queue:
  def __init__(self, queueId, params, logger):
    self.id = queueId
    self.queue = []
    self.load = 0
    self.params = params
    self.logger = logger
  
  """
  Queue length
  """
  def size(self):
    return len(self.queue)

  """
  Update all agents' observations
  """
  def updateAll(self, event):
    for agent in self.queue:
      agent.update(event)

  """
  The arrival routine. Returns (optional) scheduled depart event
  """
  def arrive(self, agent, currTime):
    self.queue.append(agent)
    self.load += agent.load
    # schedule the departure event if the queue was empty
    if len(self.queue) == 1:
      serveTime = self.queue[0].serve(self.params)
      departTime = currTime + serveTime
      event = Event(self.id, EventType.DEPART, departTime, serveTime, self.queue[0].load)
      return event
    return None

  """
  The departure routine. Returns (optional) scheduled depart event
  """
  def depart(self, currTime):
    self.logger.onDepart(currTime, self.id, self.queue[0])
    self.load -= self.queue[0].load
    self.queue = self.queue[1:]
    # schedule the departure event if the queue isn't empty
    if len(self.queue) > 0:
      serveTime = self.queue[0].serve(self.params)
      departTime = currTime + serveTime
      event = Event(self.id, EventType.DEPART, departTime, serveTime, self.queue[0].load)
      return event
    return None

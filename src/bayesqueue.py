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
  Remove agent from queue
  """
  def remove_agent(self, agent):
    self.queue.remove(agent)

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
      event = Event(self.id, EventType.DEPART, departTime, serveTime, self.queue[0].load, agent)
      return event
    
    # schedule the leave / switch event regardless (agent can always leave the queue even when others are being served)
    if agent.trials > 1:
      agent.trials -= 1
      departTime = currTime + agent.quit_time
      event = Event(self.id, EventType.SWITCH, departTime, 0, 1, agent)
      return event
    else:
      departTime = currTime + agent.quit_time
      event = Event(self.id, EventType.LEAVE, departTime, 0, 1, agent)
      return event

  """
  The departure routine. Returns (optional) scheduled depart event
  """
  def depart(self, currTime):
    self.logger.onDepart(currTime, self.id, self.queue[0])
    self.queue[0].been_served = True
    self.load -= self.queue[0].load
    self.queue = self.queue[1:]
    # schedule the departure event if the queue isn't empty
    if len(self.queue) > 0:
      serveTime = self.queue[0].serve(self.params)
      departTime = currTime + serveTime
      event = Event(self.id, EventType.DEPART, departTime, serveTime, self.queue[0].load, self.queue[0])
      return event
    return None

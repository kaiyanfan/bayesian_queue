import numpy as np

from event import Event, EventType

# stay in the current queue for at least this amount of time before switching
OBSERVE_TIME = 20

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
  Agents decide whether switching to a different queue or quit
  If the agent is being served it can't switch!
  """
  def switchAll(self, currTime):
    # cumulative load (total load in front of agent i)
    load = 0
    # work with a copy of the list as we remove from the list
    for agent in list(self.queue[1:]):
      # must observe for a certain amount of time before switching
      if agent.arrivalTime + OBSERVE_TIME > currTime:
        load += agent.load
        continue
      dst = agent.select_posterior(self.queues, self.id, load)
      # Quit the queue
      if dst == None:
        self.queue.remove(agent)
        self.load -= agent.load
        self.logger.onLeave(currTime, agent, self.id)
      # Switch to a different queue
      elif dst != self.id:
        self.queue.remove(agent)
        self.load -= agent.load
        self.queues[dst].arrive(agent, currTime)
        self.logger.onSwitch(currTime, agent, self.id, dst)
      # Add to cumulative load
      load += agent.load

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

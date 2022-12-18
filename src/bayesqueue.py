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
  def updateAll(self, fromQueue, toQueue):
    for agent in self.queue:
      agent.update(fromQueue, toQueue)
  
  """
  Agents decide whether switching to a different queue or quit
  If the agent is being served it can't switch!
  """
  def switchAll(self, currTime):
    # cumulative load (total load in front of agent i)
    load = 0
    # work with a copy of the list as we remove from the list
    for i, agent in enumerate(list(self.queue[1:])):
      # must observe for a certain amount of time before switching
      # if agent.arrivalTime + OBSERVE_TIME > currTime:
      #   load += agent.load
      #   continue
      dst = agent.select_posterior(self.id)
      # Quit the queue
      # if dst == None:
      #   self.queue.remove(agent)
      #   self.load -= agent.load
      #   self.logger.onLeave(currTime, agent, self.id)
      # Switch to a different queue
      if dst != self.id:
        self.queue.remove(agent)
        # self.load -= agent.load
        self.queues[dst].arrive(agent, currTime, i)
        self.logger.onSwitch(currTime, agent, self.id, dst)
        for q in self.queues:
          q.updateAll(self.id, dst)

      # Add to cumulative load
      # load += agent.load

  """
  The arrival routine. Returns (optional) scheduled depart event
  """
  def arrive(self, agent, currTime, index=0):
    if index == 0:
      self.queue.append(agent)
    else:
      self.queue.insert(index, agent)
    # schedule the departure event if the queue was empty
    if len(self.queue) == 1:
      serveTime = self.queue[0].serve(self.params)
      departTime = currTime + serveTime
      event = Event(self.id, EventType.DEPART, departTime, serveTime, 1, agent)
      return event
    
  """
  The departure routine. Returns (optional) scheduled depart event
  """
  def depart(self, currTime):
    self.logger.onDepart(currTime, self.id, self.queue[0])
    self.queue[0].been_served = True
    self.queue = self.queue[1:]
    # schedule the departure event if the queue isn't empty
    if len(self.queue) > 0:
      serveTime = self.queue[0].serve(self.params)
      departTime = currTime + serveTime
      event = Event(self.id, EventType.DEPART, departTime, serveTime, 1, self.queue[0])
      return event
    return None

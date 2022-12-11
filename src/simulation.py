import heapq
import json
import numpy as np

from agents.mallcustomer import MallCustomer

from event import Event, EventType
from bayesqueue import Queue
from logger import Logger

config = "../configs/mall01.json"

class Simulation:
  def __init__(self, agentType, arrivalLam, numQueue, queueParams, simTime):
    self.agentType = agentType
    # all scheduled events; priority queue
    self.events = []
    self.arrivalLam = arrivalLam
    self.time = 0
    self.runtime = simTime
    self.logger = Logger(numQueue)
    # list of all queues
    self.__initQueue(numQueue, queueParams)

  def __initQueue(self, numQueue, queueParams):
    self.numQueue = numQueue
    self.queues = []
    for i in range(numQueue):
      self.queues.append(Queue(i, queueParams[i], self.logger))

  """
  Calculate the time for the next arrival event
  """
  def __scheduleTime(self):
    # arrival is a poisson process
    time = np.random.poisson(self.arrivalLam)
    return time
  
  """
  Schedule the next arrival event
  """
  def __schedule(self):
    time = self.time + self.__scheduleTime()
    # queue = 0 is a placeholder. Which queue to join is decided at arrival
    event = Event(0, EventType.ARRIVAL, time)
    heapq.heappush(self.events, event)

  """
  On arrival event
  """
  def __arrive(self, event):
    agent = self.agentType(self.time, self.numQueue)
    queue_idx = agent.select_queue(self.queues)
    agent.initQueue = queue_idx
    agent.currQeueu = queue_idx
    self.logger.onArrival(self.time, queue_idx, agent)

    nextEvent = self.queues[queue_idx].arrive(agent, self.time)
    if nextEvent != None:
      heapq.heappush(self.events, nextEvent)

  """
  On departure event
  """
  def __depart(self, event):
    queue = event.queue
    nextEvent = self.queues[queue].depart(self.time)
    # update all agents' observations
    for q in self.queues:
      q.updateAll(event)
    if nextEvent != None:
      heapq.heappush(self.events, nextEvent)

  def run(self):
    print("Simulation begins")
    # first, schedule an arrival
    self.__schedule()

    # event loop
    while True:
      # the event queue should never be empty!
      assert (len(self.events) > 0)
      # simulation ends
      if self.time > self.runtime:
        print("Simulation ends")
        break
      # pick up the next event
      event = heapq.heappop(self.events)
      # trigger the event
      self.time = event.eventTime
      if event.eventType == EventType.ARRIVAL:
        self.__arrive(event)
        self.__schedule()
      else:
        self.__depart(event)
      # update agents' understanding of the queue
    
    self.logger.report()

def simulate():
  f = open(config)
  configs = json.load(f)
  try:
    simTime = configs["sim_time"]
    simType = configs["type"]
    numQueue = configs["num_queue"]
    arrivalLam = configs["arrival_lam"]
    params = configs["queue_params"]
  except:
    raise Exception("Config Error")

  if simType == "mallcustomer":
    agentType = MallCustomer
  else:
    raise Exception(f"Unknown simulation type {simType}")

  sim = Simulation(agentType, arrivalLam, numQueue, params, simTime)
  sim.run()

if __name__ == "__main__":
  simulate()

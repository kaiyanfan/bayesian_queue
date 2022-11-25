import heapq
import json

from agent import Agent
from event import Event, EventType
from queue import Queue

class Simulation:
  def __init__(self, arrivalMu, numQueue, departMu, simTime):
    # list of all queues
    self.__initQueue(numQueue, departMu)
    # all scheduled events; priority queue
    self.events = []
    self.mu = arrivalMu
    self.time = 0
    self.runtime = simTime

  def __initQueue(self, numQueue, departMu):
    self.queues = []
    for i in range(numQueue):
      self.queues.append(Queue(i, departMu[i]))

  """
  Calculate the time for the next arrival event
  """
  def __scheduleTime(self):
    # TODO: make this probablistic
    return 1
  
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
    agent = Agent()
    # TODO: join the right queue
    queue = 0
    print(f"Agent {agent.id} arrives queue {queue} at {self.time}")

    nextEvent = self.queues[queue].arrive(agent, self.time)
    if nextEvent != None:
      heapq.heappush(self.events, nextEvent)

  """
  On departure event
  """
  def __depart(self, event):
    queue = event.queue
    nextEvent = self.queues[queue].depart(self.time)
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
      # time travel
      self.time = event.eventTime
      if event.eventType == EventType.ARRIVAL:
        self.__arrive(event)
        self.__schedule()
      else:
        self.__depart(event)

def simulate():
  f = open("../qconfig.json")
  configs = json.load(f)
  try:
    arrivalMu = configs["arrival_mu"]
    numQueue = configs["num_queue"]
    departMu = configs["depart_mu"]
    simTime = configs["sim_time"]
  except:
    print("Config Error")
    return

  sim = Simulation(arrivalMu, numQueue, departMu, simTime)
  sim.run()

if __name__ == "__main__":
  simulate()

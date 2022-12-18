from agents.agent import Agent

# models the *default effect*: people tend to stay at where they are unless there is a big difference in queueing time
SWITCH_THRESHOLD = 1.1

class HighwayCar(Agent):

  def __init__(self, arrivalTime, numQueue):
    # posterior service speed estimation for each queue
    self.served = [0 for _ in range(numQueue)]
    self.numQueue = numQueue
    
    super().__init__(arrivalTime)
  
  """
  Select the fastest queue based on the posterior estimates on queue speed
  currLoad: the current load that agent waits for
  """
  def select_posterior(self, currQueue):
    left = currQueue - 1
    right = currQueue + 1
    if left >= 0 and self.served[left] > self.served[currQueue] + 1:
      return left
    if right < self.numQueue and self.served[right] > self.served[currQueue] + 1:
      return right
    return currQueue
  
  """
  Update the agent's view of the queue states
  """
  def update(self, fromQueue, toQueue):
    self.served[fromQueue] += 1
    if toQueue is not None:
      self.served[toQueue] -= 1
  
  """
  params: parameters for the service speed
  param[0]: mu, expected service speed
  param[1]: sigma, s.d. of the service speed
  """
  def serve(self, params):
    return params[0]

  def select_queue(self, queues):
    return super().select_shortest(queues)

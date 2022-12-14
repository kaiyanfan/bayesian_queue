import random
import numpy as np

from agents.agent import Agent, SelectionCriteria

MIN_LOAD = 10
MAX_LOAD = 30

# conjugate prior (µ, λ)
# prior mean
PRIOR_MU = 1
# prior lambda; represents how strong does the agent believe in the prior mean
PRIOR_LAMBDA = 3
# models the *default effect*: people tend to stay at where they are unless there is a big difference in queueing time
SWITCH_THRESHOLD = 1.1
# max waiting time
MAX_WAIT = 300

class HumanAgent(Agent):

  """
  Load is a uniform distribution from MIN_LOAD to MAX_LOAD
  """
  def __init_load(self):
    self.load = random.randint(MIN_LOAD, MAX_LOAD)

  def __init__(self, arrivalTime, numQueue):
    self.__init_load()
    # posterior service speed estimation for each queue
    self.speeds = [PRIOR_MU for _ in range(numQueue)]
    # sum of service speed for each queue, **observed by this agent**
    self.speedSum = [0 for _ in range(numQueue)]
    # number of served customer for each queue, **observed by this agent**
    self.served = [0 for _ in range(numQueue)]
    
    super().__init__(arrivalTime)

  """
  Bayesian estimation of normal distribution (unknown variance). NormalGamma distribution
  Luckily, the inference is very simplified as we only care about the mean μ
  https://www.cs.ubc.ca/~murphyk/Papers/bayesGauss.pdf

  Instead of doing consecutive inferences, we accumulate the data and always do a single inference
  on the prior
  
  Returns the posterior mean
  """
  def __infer(self, n, lam, sumData, prior):
    return 1 / (n + lam) * (sumData + lam * prior)
  
  """
  Select the fastest queue based on the posterior estimates on queue speed
  currLoad: the current load that agent waits for
  """
  def select_posterior(self, queues, currQueue, currLoad):
    # human agents do not switch in this experiment
    return currQueue
  
  """
  Update the agent's view of the queue states
  """
  def update(self, event):
    queue = event.queue
    speed = event.serveTime / event.load
    # update this agent's observations
    self.speedSum[queue] += speed
    self.served[queue] += 1
    # bayesian inference on normal distribution
    self.speeds[queue] = self.__infer(self.served[queue], PRIOR_LAMBDA, self.speedSum[queue], PRIOR_MU)

  """
  params: parameters for the service speed
  param[0]: mu, expected service speed
  param[1]: sigma, s.d. of the service speed
  """
  def serve(self, params):
    mu = params[0]
    sigma = params[1]
    # at least takes 1 time unit to serve
    return max(1, np.random.normal(mu, sigma) * self.load)

  def select_queue(self, queues):
    print("\tAgent has load", self.load)

    for i, q in enumerate(queues):
      print("\tQueue", i, ": ", q.pretty_string())
    
    selected_queue = int(input('\tselect queue by index: '))

    while (selected_queue < 0 or selected_queue >= len(queues)):
        selected_queue = int(input('\tindex out of range, try again: '))

    return selected_queue

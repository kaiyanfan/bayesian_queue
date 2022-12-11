import random
import numpy as np

from agents.agent import Agent

MIN_LOAD = 10
MAX_LOAD = 30

class MallCustomer(Agent):

  """
  Load is a uniform distribution from MIN_LOAD to MAX_LOAD
  """
  def __init_load(self):
    self.load = random.randint(MIN_LOAD, MAX_LOAD)

  def __init__(self, arrivalTime):
    self.__init_load()
    super().__init__(arrivalTime)

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

from enum import Enum
import random

class ObservedLoad(Enum):
  SMALL = 0
  MEDIUM = 1
  LARGE = 2

class SelectionCriteria(Enum):
  FEWEST = 0
  SHORTEST_OBSERVED = 1
  
global_id = 0

class Agent:

  def __init_load(self, probability_table = [[0.8, 0.15, 0.05], [0.2, 0.6, 0.2], [0.05, 0.15, 0.8]]):
    slice_a, slice_b = random.choices(population = [[0, 50], [25, 75], [75, 100]], weights=probability_table[self.observed_load.value], k = 1)[0]
    # slice [1, 100] into intervals and random sample
    self.load_time = random.randint(slice_a, slice_b)

  def __init__(self, select_how=SelectionCriteria.SHORTEST_OBSERVED):
    global global_id
    self.id = global_id
    global_id += 1
    
    """
    true load_time given observed load in {small, medium, large}
    load type         |  small  |  medium  |  large  | 
    -------------------------------------------------
    P(Unif[0, 50])    |  0.8    |  0.2     |  0.05   | 
    P(Unif[25, 75])   |  0.15   |  0.6     |  0.15   | 
    P(Unif[50, 100])  |  0.05   |  0.2     |  0.8    | 
    """
    self.load_time = 0
    self.observed_load = ObservedLoad.MEDIUM
    self.patience_time = 999999
    self.selection_time = 0
    self.select_how = select_how

    self.__init_load()

  def __select_queue_fewest(self, queues):
    shortest, shortestLen = 0, queues[0].size()
    for i, q in enumerate(queues):
      # print("\tqueue ", i, " with len ", q.size())
      if q.size() < shortestLen:
        shortest, shortestLen = i, q.size()
    return shortest
  
  def __select_queue_shortest_observed(self, queues):
    shortest, shortestLen = 0, queues[0].get_observed_load()
    for i, q in enumerate(queues):
      if q.size() < shortestLen:
        shortest, shortestLen = i, q.get_observed_load()
    return shortest

  def select_queue(self, queues):
    if self.select_how == SelectionCriteria.FEWEST:
      return self.__select_queue_fewest(queues)
    elif self.select_how == SelectionCriteria.SHORTEST_OBSERVED:
      return self.__select_queue_shortest_observed(queues)
    




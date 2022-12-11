"""
Report the following statistics at every timestamp
1. The length of every queue
2. The average wait time of each queue

Report the following statistics at the very end
3. The total customers served at every queue
4. The total number of arrivals at every queue
5. The total number of customers leaving a queue halfway
6. The total number of customers joining the queue halfway
"""

import csv
from enum import Enum
import matplotlib.pyplot as plt

class Row(Enum):
  SERVED = 0
  ARRIVAL = 1
  LEAVE = 2
  JOIN = 3

class Logger:
  def __init__(self, numQueue):
    self.queueLen = [{} for _ in range(numQueue)]
    self.queueStat = [[0, 0, 0, 0] for _ in range(numQueue)]
    # current length
    self.currLen = [0] * numQueue

  def onArrival(self, time, queue):
    self.queueStat[queue][Row.ARRIVAL.value] += 1
    self.currLen[queue] += 1
    self.queueLen[queue][time] = self.currLen[queue]

  def onDepart(self, time, queue):
    self.queueStat[queue][Row.SERVED.value] += 1
    self.currLen[queue] -= 1
    self.queueLen[queue][time] = self.currLen[queue]

  def onSwitch(self, time, fromQueue, toQueue):
    pass

  def onLeave(self, time, queue):
    pass

  def report(self):
    # Report to csv
    header = ['Queue ID', 'Num Served', 'Num Arrival', 'Num Left halfway', 'Num Join halfway']
    with open('report.csv', 'w') as f:
      writer = csv.writer(f)
      writer.writerow(header)
      for i, row in enumerate(self.queueStat):
        row_ = [i] + row
        writer.writerow(row_)

    # Report to diagrams
    for i, length in enumerate(self.queueLen):
      lists = sorted(length.items())
      x, y = zip(*lists)
      plt.plot(x, y, label = f'Queue {i}')
    plt.xlabel("Time (s)")
    plt.ylabel("Queue Length")
    plt.legend()
    plt.show()


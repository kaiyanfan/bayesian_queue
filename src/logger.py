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
    self.queueLen = [{0: 0} for _ in range(numQueue)]
    self.waitTime = [{} for _ in range(numQueue)]
    self.totalWaitTime = [(0, 0) for _ in range(numQueue)]
    self.queueStat = [[0, 0, 0, 0] for _ in range(numQueue)]
    # current length
    self.currLen = [0] * numQueue

  def onArrival(self, time, queue, agent):
    print(f"Agent {agent.id} arrives queue {queue} at {time}")
    self.queueStat[queue][Row.ARRIVAL.value] += 1
    self.currLen[queue] += 1
    self.queueLen[queue][time] = self.currLen[queue]

  def onDepart(self, time, queue, agent):
    print(f"Agent {agent.id} departs queue {queue} at {time}")
    self.queueStat[queue][Row.SERVED.value] += 1
    self.currLen[queue] -= 1
    self.queueLen[queue][time] = self.currLen[queue]

    # updates average wait time statistics
    initQueue = agent.initQueue
    count, totalTime = self.totalWaitTime[initQueue]
    self.totalWaitTime[initQueue] = (count + 1, totalTime + time - agent.arrivalTime)
    self.waitTime[initQueue][time] = self.totalWaitTime[initQueue][1] / self.totalWaitTime[initQueue][0]

  def onSwitch(self, time, agent, fromQueue, toQueue):
    print(f"Agent {agent.id} switches from queue {fromQueue} to queue {toQueue} at {time}")
    self.queueStat[fromQueue][Row.LEAVE.value] += 1
    self.currLen[fromQueue] -= 1
    self.queueLen[fromQueue][time] = self.currLen[fromQueue]

    self.queueStat[toQueue][Row.JOIN.value] += 1
    self.currLen[toQueue] += 1
    self.queueLen[toQueue][time] = self.currLen[toQueue]

    initQueue = agent.initQueue
    currQeueu = agent.currQeueu
    count, totalTime = self.totalWaitTime[initQueue]
    self.totalWaitTime[initQueue] = (count + 1, totalTime + time - agent.arrivalTime)
    self.waitTime[initQueue][time] = self.totalWaitTime[initQueue][1] / self.totalWaitTime[initQueue][0]

  def onLeave(self, time, agent, queue):
    print(f"Agent {agent.id} quits queue {queue} at {time}")
    self.queueStat[queue][Row.LEAVE.value] += 1
    self.currLen[queue] -= 1
    self.queueLen[queue][time] = self.currLen[queue]

    # updates average wait time statistics
    initQueue = agent.initQueue
    currQeueu = agent.currQeueu
    count, totalTime = self.totalWaitTime[currQeueu]
    self.totalWaitTime[currQeueu] = (count + 1, totalTime + time - agent.arrivalTime)
    self.waitTime[currQeueu][time] = self.totalWaitTime[currQeueu][1] / self.totalWaitTime[currQeueu][0]

  def report(self):
    # Report to csv
    header = ['Queue ID', 'Num Served', 'Num Arrival', 'Num Left halfway', 'Num Join halfway']
    with open('../reports/report.csv', 'w') as f:
      writer = csv.writer(f)
      writer.writerow(header)
      for i, row in enumerate(self.queueStat):
        row_ = [i] + row
        writer.writerow(row_)

    # Report queue length statistics to diagram
    plt.figure(0)
    for i, length in enumerate(self.queueLen):
      lists = sorted(length.items())
      x, y = zip(*lists)
      plt.plot(x, y, label = f'Queue {i}')
    plt.xlabel("Time (s)")
    plt.ylabel("Queue Length")
    plt.legend()
    plt.savefig('../reports/length.png')

    # report wait time statistics to diagram
    plt.figure(1)
    # print(self.waitTime)
    for i, length in enumerate(self.waitTime):
      lists = sorted(length.items())
      x, y = zip(*lists)
      plt.plot(x, y, label = f'Queue {i}')
    plt.xlabel("Time (s)")
    plt.ylabel("Average Wait Time(s)")
    plt.legend()
    plt.savefig('../reports/waittime.png')

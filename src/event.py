from enum import Enum

class EventType(Enum):
  ARRIVAL = 1
  DEPART = 2

class Event:
  def __init__(self, queue, eventType, eventTime, serveTime=0, load=1):
    self.queue = queue
    self.eventType = eventType
    self.eventTime = eventTime
    self.serveTime = serveTime   # used by DEPART event only
    self.load = load             # used by DEPART event only

  # ordered by event time
  def __lt__(self, other):
    return self.eventTime < other.eventTime

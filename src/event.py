from enum import Enum

class EventType(Enum):
  ARRIVAL = 1
  DEPART = 2

class Event:
  def __init__(self, queue, eventType, eventTime):
    self.queue = queue
    self.eventType = eventType
    self.eventTime = eventTime

  # ordered by event time
  def __lt__(self, other):
    return self.eventTime < other.eventTime

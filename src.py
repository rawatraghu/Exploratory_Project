# from distutils.log import error
# from logging import raiseExceptions
import math
# import re

bandwidth = 868     # MHz
velocity = 10       # in m/s
TotalflightTime = 10
TotalFlightDis = velocity*TotalflightTime
LoRaDutyCycle = 6

class Node:
    def __init__(self, x, y, priority, data):
        self.x = x           # in m
        self.y = y           # in m
        self.priority = priority
        self.data = data     # in KB
        self.HoveringTime = min(self.data/bandwidth, LoRaDutyCycle)     # in sec
        self.visited = False

    def __str__(self):
        return f'({self.x}, {self.y})'
    
    def __repr__(self):
        return f'({self.x}, {self.y})'
    
    def __eq__(self, node):
        if node.x == self.x and node.y == self.y:
            if node.priority != self.priority or node.data != self.data:
                raise Exception('Node at one location can not have multiple priority or data')
            return True
        return False
    
    def fn(self):
        return bandwidth*self.HoveringTime

    def utility(self):
        return self.fn()*self.priority

def Distance(n1, n2):
    return math.sqrt(pow(n1.x - n2.x, 2) + pow(n1.y - n2.y, 2))

def manhatanDistance(n1, n2):
    return abs(n1.x - n2.x) + abs(n1.y - n2.y)

def costUAV(n1, n2):
    return math.ceil((n1.HoveringTime + n2.HoveringTime)/2 + Distance(n1, n2)/velocity)

def costUGV(n1, n2):
    return math.ceil((n1.HoveringTime + n2.HoveringTime)/2 + manhatanDistance(n1, n2)/velocity)
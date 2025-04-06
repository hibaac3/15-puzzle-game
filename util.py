#!/usr/bin/env python3
"""
util.py

Data structures used by search.py
"""

import heapq
import sys

class Stack:
    def __init__(self):
        self.list = []

    def push(self, item):
        self.list.append(item)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list) == 0

    def size(self):
        return len(self.list)

class Queue:
    def __init__(self):
        self.list = []

    def push(self, item):
        # front is the end of the list
        self.list.insert(0, item)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list) == 0

    def size(self):
        return len(self.list)

class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        heapq.heappush(self.heap, (priority, self.count, item))
        self.count += 1

    def pop(self):
        (p, c, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def size(self):
        return len(self.heap)

    def update(self, item, priority):
        """
        If item is in queue with higher priority, update it. Otherwise push new.
        """
        for idx, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    return
                del self.heap[idx]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                return
        self.push(item, priority)

def raiseNotDefined():
    print("Method not implemented.")
    sys.exit(1)

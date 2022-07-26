from collections import deque, Counter
import threading
from .anrequest import AnRequest
import logging

class Q:
    r : AnRequest
    """The address who make the oracle call"""

    def __init__(self,invoke,r):
        """Create a new action request."""
        self.invoke = invoke
        self.r = r


    def call(self):
        t = threading.Thread(target = self.invoke, args=(self.r,))
        t.start()

class Queue:
    threads : int
    """Max action running at the same time."""
    actions : dict
    """Pre-defined function based key-index dictionary"""
    def __init__(self,actions,threads = 1):
        """Create a FIFO actions request manager."""
        self.threads = threads  # Max actions running at the same time.
        self.actions = actions
        self.que = deque()


    def enqueue(self,request):
        """Add action ready to be callable."""

        action_exe = self.actions.get(request.getAction())
        if(action_exe != None):
            logging.info('Sender: %s call: %s',request.getSender(),request.getAction())
            self.que.append(Q(action_exe,request))
        else:
            logging.warning('%s Trying to call: %s, action do not exist!',request.getSender(),request.getAction())

    def dequeue(self):
        """Call the next action available."""
        if(len(self.que) > 0):
            if threading.active_count()-1 < int(self.threads):
                action = self.que.popleft()
                action.call()
            else:
                logging.warning('Max threads running')

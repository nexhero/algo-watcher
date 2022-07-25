from collections import deque, Counter
import threading
import logging

class Q:
    caller :str
    """The address who make the oracle call"""
    invoke :str
    """The callback function."""
    metadata : dict
    """Argument passed to the invoke function."""
    def __init__(self,caller,invoke, metadata = None):
        """Create a new action request."""
        self.caller = caller
        self.metadata = metadata
        self.invoke = invoke


    def call(self):
        if(self.metadata != None):
            t = threading.Thread(target = self.invoke, args=(self.metadata,))
        else:
            t = threading.Thread(target = self.invoke)
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
    def enqueue(self,sender,action_index,data = None):
        """Add action ready to be callable."""
        # TODO: Add loggin support
        action_exe = self.actions.get(action_index)
        if(action_exe != None):
            logging.info('Sender: %s call: %s',sender,action_index)
            self.que.append(Q(sender,action_exe,data))
        else:
            logging.warning('%s Trying to call: %s, action do not exist!',sender,action_index)

    def dequeue(self):
        """Call the next action available."""
        if(len(self.que) > 0):
            if threading.active_count()-1 < int(self.threads):
                action = self.que.popleft()
                action.call()
            else:
                logging.warning('Max threads running')

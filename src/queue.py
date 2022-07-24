from collections import deque, Counter
import threading
import logging
class Q:
    """"""
    def __init__(self,caller,invoke, metadata = None):
        """
        Parameters
        caller: String the sender address
        metadata: String the note message
        invoke: The callback function
        """
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
    """"""
    def __init__(self,actions,threads = 1):
        self.threads = threads  # Max actions running at the same time.
        self.actions = actions
        self.que = deque()
    def enqueue(self,sender,action_index,data = None):
        """Add action to run """
        # TODO: Add loggin support
        action_exe = self.actions.get(action_index)
        if(action_exe != None):
            logging.info('Sender: %s call: %s',sender,action_index)
            self.que.append(Q(sender,action_exe,data))
        else:
            logging.warning('%s Trying to call: %s, action do not exist!',sender,action_index)

    def dequeue(self):
        """Execute the first action """
        # TODO: Add loggin support
        # print("Currect active threads: " + str(threading.active_count()-1) + "of " + str(self.threads))
        if(len(self.que) > 0):
            if threading.active_count()-1 < int(self.threads):
                action = self.que.popleft()
                action.call()
            else:
                logging.warning('Max threads running')

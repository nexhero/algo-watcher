"""
Algo Watcher use note field from payment transaction as Json request to run actions offchain on Algorand.\n
example for a note using Json: \n
`{
  "app": "test1",
  "action": "hello",
  "data": {
    "name": "Wattson",
  }
}`
"""
from algosdk.v2client.indexer import IndexerClient
import json
import base64
from .queue import Q, Queue
import time
import logging
import sys


class watcher:
    algo_toke :str
    """ Algorand Indexer token."""
    algo_addr :str
    """Algorand Indexer host address."""
    app :str
    """Unique app name that watcher reconize."""
    actions : dict
    """Store functions based on keys indexes that serves as callbacks."""
    oracle_addr : str
    """The payment transaction reciever."""
    threads : int
    """Total actions that `algo-watcher` can run at the same time."""
    at_round : int
    """Initial round that watcher start seek for oracle call."""
    to_round : int
    """
    If this parameter is not defined, the oracle app will seek for every new round generated.
    Otherwise it will end the program to the round defined.
    """

    def __init__(self,algo_token, algo_addr, app,actions,oracle_addr,threads = 1, at_round = 1, to_round = None):
        """Make a watcher client object."""
        self.algo_token = algo_token
        self.algo_addr = algo_addr
        self.app = app
        self.actions = actions
        self.oracle = oracle_addr
        self.threads = threads
        self._round = at_round
        self.to_round = to_round

        self.queue = Queue(actions,self.threads)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("oracle.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )

        headers = {
            "X-API-Key": self.algo_token
        }

        # create the indexer client
        self.indexer = IndexerClient(self.algo_token, self.algo_addr,headers)

    def loop(self):
        """Run time that check every block until reconize oracle call and actions"""
        loop_on = True
        while loop_on:
            if self.to_round == None or self._round <= self.to_round:
                self.__fetch()
                self.queue.dequeue()
                time.sleep(4.5)
            else:
                loop_on = False


    def __serialize(self,response):
        """private function"""
        for txn in response['transactions']:
            pay_transaction = txn.get("payment-transaction")
            txn_id = txn['id']
            sender = txn.get('sender')
            if pay_transaction != None:
                if pay_transaction['receiver'] == self.oracle:
                    # Check if the note is a valid json
                    try:
                        metadata = json.loads(base64.b64decode(txn['note']).decode('utf-8'))
                    except json.decoder.JSONDecodeError:
                        logging.error('Transaction: %s Sender: %s | Note is not a JSON request!',txn_id,sender)
                        # print("Note is not a valid json")
                    else:
                        # check for the app name
                        app = metadata.get('app')
                        action = metadata.get('action')
                        data = metadata.get('data')
                        if(app == None or app != self.app):
                            logging.error('Transaction: %s Sender: %s | app-id incorrect!',txn_id,sender)
                            return 0
                        elif(action == None or action == ''):
                            logging.error('Transaction: %s Sender: %s | No action found!',txn_id,sender)
                            return 0
                        else:
                            self.queue.enqueue(sender,action,data)
            # else:
                # print("No transaction found on round: " + str(self._round))

    def __fetch(self):
        """"""
        logging.info('Checking round: %s',str(self._round))
        response = self.indexer.block_info(round_num=self._round)
        self.__serialize(response)
        self._round += 1

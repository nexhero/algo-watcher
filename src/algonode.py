from algosdk.v2client.indexer import IndexerClient
from algosdk.v2client.algod import AlgodClient
from algosdk import account, encoding, mnemonic, future
from algosdk.future import transaction
import datetime
import logging
class Manager:
    """Manage request to a node"""
    algo_token :str
    """ Algorand Indexer token."""
    algod_addr :str
    """Algorand Algod host address."""
    index_addr: str
    """Algorand Indexer host address."""
    oracle : str
    """mnmonic for the payment transaction reciever."""
    smartcontract :int
    """Smartcontract app id."""
    rps: int
    """Request per second, this variable manage how many request you can do before the node blocks the application."""

    def __init__(self, algo_token, algod_addr,index_addr, oracle,smartcontract = None,rps = 3):
        self.algo_token = algo_token
        self.algod_addr = algod_addr
        self.index_addr = index_addr
        self.oracle = oracle
        self.smartcontract = smartcontract
        self.rps = rps
        self.r_tracker = 0      # track the request per second
        self.time_snapshot = datetime.datetime.now() # Store the time for each request to the node.
        headers = {
            "X-API-Key": self.algo_token
        }
        self.algo_client = AlgodClient(self.algo_token,self.algod_addr,headers)
        self.indexer = IndexerClient(self.algo_token,self.index_addr,headers)
        self.sk = mnemonic.to_private_key(self.oracle) # secret key for the oracle
        self.pk = mnemonic.to_public_key(self.oracle)  # public key for the oracle

    def __add_rps_time(self):
        """Increment by 1 the rps"""
        now = datetime.datetime.now()
        dt = now - self.time_snapshot
        if self.r_tracker < self.rps and dt.total_seconds() < 1:
            self.r_tracker += 1
            self.time_snapshot = datetime.datetime.now()
        if dt.total_seconds() > 1:
            self.r_tracker = 0


    def rps_status(self):
        """Return True if the request tracker is lower to rps"""
        if self.r_tracker < self.rps:
            return True
        else:
            return False

    def __wait_rps(self):
        """If the rps is at its max, wait until to continue."""
        while self.rps_status() != True:
            now = datetime.datetime.now()
            logging.info("RPS: %s",manager.rps)
            dt = now - self.time_snapshot
            if dt.total_seconds() > 1:
                self.r_tracker = 0;

    def __sp(self):
        """Get the suggested params"""
        self.__wait_rps()
        sp = self.algo_client.suggested_params()
        self.__add_rps_time()
        return sp
    def makePayment(self,receiver,amt,close_remainder_to=None,note=None,lease=None,rekey_to=None):
        self.__wait_rps()
        sp = self.__sp()
        txn = future.transaction.PaymentTxn(self.pk,sp,receiver,amt,close_remainder_to,note,lease,rekey_to)
        signedTxn = txn.sign(self.sk)
        txn_id = signedTxn.transaction.get_txid()
        self.algo_client.send_transaction(signedTxn)
        self.__add_rps_time()
        logging.info("RPS on manager: %s",str(self.r_tracker))

    def status(self):
        """Get the algod client status."""
        self.__wait_rps()
        response =  self.algo_client.status()
        self.__add_rps_time()
        return response
    def getBlock(self,rn):
        """Get the currect blocks transactions."""
        # Wait until we can make a request
        self.__wait_rps()
        response = self.indexer.block_info(round_num=rn) # Make the request
        # Update the rps tracker.
        self.__add_rps_time()
        return response

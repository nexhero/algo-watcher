class AnRequest:
    """Define a basic Algorand Note Request"""

    am : object
    """The  algonode.Manager object"""
    txn :str
    """Transacction id where the action was called"""
    sender :str
    """User who make the request to the oracle"""
    body :dict
    """Note Request content"""
    # TODO: rewrite documentation
    def __init__(self,am,txn,sender,body):
        self.txn = txn
        self.sender = sender
        self.body = body
        self.am = am

    def getManager(self):
        """Return the node manager object, this enable to use algod and indexer clients into each action function"""
        return self.am
    def getTxn(self):
        """Return the transaction id"""
        return self.txn

    def getSender(self):
        """Return the sender address"""
        return self.sender

    def getAppId(self):
        """Get the oracle app id"""
        return self.body['app']

    def getAction(self):
        """Get the Action name for the request"""
        return self.body['action']

    def getData(self):
        """Get the data passed to the function"""
        return self.body['data']

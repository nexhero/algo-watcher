class AnRequest:
    """Define a basic Algorand Note Request"""

    txn :str
    """Transacction id where the action was called"""
    sender :str
    """User who make the request to the oracle"""
    body :dict
    """Note Request content"""
    def __init__(self,txn,sender,body):
        self.txn = txn
        self.sender = sender
        self.body = body

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

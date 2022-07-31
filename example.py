#!/bin/python3
"""
Small example for the Algo Watcher client \n
It will check between two round seeking for `test1` oracle app
and execute `hello()` and `add()` function. \n
Example transaction: \
https://testnet.algoexplorer.io/tx/RDXTSMGDP4Q4BJ2NVPOPOEQ6OXZ4NTLCNX7PX6MVYC6THMIX7YJQ
"""
from src import watcher
import logging
import time

"""
Purestake secret sauce\n
https://developer.purestake.io/home
"""
token = "" # Add purestake secret token
index_addr = "https://testnet-algorand.api.purestake.io/idx2"
algod_addr = "https://testnet-algorand.api.purestake.io/ps2"
"""Indexer host"""
app = "test1"

oracle =""


"""Initial round"""
f_round = 23035719
"""Stop seek for oracle call at this block"""
t_round = 23035735
actions : dict
"""Define actions"""

def hello(r = None):
    """Callback function for the action hello"""
    data = r.getData()
    manager = r.getManager()
    if( data  != None ):
        name = data['name']
        sleep_for = data['sleep']
        logging.info("Hello %s",name)
        time.sleep(sleep_for+17.2)
        manager.makePayment(r.getSender(),1000,note="pay back!")
        logging.info("Bye %s", name)
    else:
        logging.error("No data args")


def add(r):
    "Callback function for the action add"
    data = r.getData()
    manager = r.getManager()
    n1 = data['n1']
    n2 = data['n2']
    logging.info("Called add() | Return:%s",str(n1+n2))


actions = {
    'hello':hello,
    'add':add
}

if __name__ =="__main__":
    w = watcher(
        algo_token = token,
        algod_addr = algod_addr,
        index_addr = index_addr,
        app_name = app,
        actions = actions,
        oracle = oracle,
        rps = 3,
        threads = 2,
        at_round = f_round,
        to_round =  t_round +1
    )
    w.loop()

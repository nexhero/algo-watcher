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
token = "" # Add purestake secret token
"""
Purestake secret sauce\n
https://developer.purestake.io/home
"""
addr = "https://testnet-algorand.api.purestake.io/idx2"
"""Indexer host"""
app = "test1"
"""app unique name"""
oracle = "MIG24V2QZ7JKGUZSB2TNY7WMG3MY3PLVCVIWV7WMBMWRR2PQF3S6XB44CM"
"""Oracle Address"""
f_round = 23035719
"""Initial round"""
t_round = 23035735
"""Stop seek for oracle call at this block"""
actions : dict
"""Define actions"""

def hello(r = None):
    """Callback function for the action hello"""
    data = r.getData()
    if( data  != None ):
        name = data['name']
        sleep_for = data['sleep']
        logging.info("Hello %s",name)
        time.sleep(sleep_for+17.2)
        logging.info("Bye %s", name)
    else:
        logging.error("No data args")


def add(r):
    "Callback function for the action add"
    data = r.getData()
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
        algo_addr = addr,
        app = app,
        actions = actions,
        oracle_addr = oracle,
        threads = 2,
        at_round = f_round,
        to_round =  t_round +1
    )
    w.loop()

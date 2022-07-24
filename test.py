from src import watcher
import logging
import time
token = "" # Add purestake secret token
addr = "https://testnet-algorand.api.purestake.io/idx2"
app = "test1"
oracle = "MIG24V2QZ7JKGUZSB2TNY7WMG3MY3PLVCVIWV7WMBMWRR2PQF3S6XB44CM"
# _round = 23031488               # valid call
# _round = 23033698               # invalid call
f_round = 23035719               # invalid action
t_round = 23035735               # no data
def hello(data = None):
    if( data  != None ):
        name = data['name']
        sleep_for = data['sleep']
        logging.info("Hello %s",name)
        time.sleep(sleep_for+17.2)
        logging.info("Bye %s", name)
    else:
        logging.error("No data args")
def add(data):
    n1 = data['n1']
    n2 = data['n2']
    logging.info("Called add() | Return:%s",str(n1+n2))
actions = {
    'hello':hello,
    'add':add
}
# serializer(data,oracle)
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

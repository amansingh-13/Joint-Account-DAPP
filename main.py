from web3 import *
import time 


from Dapp import Dapp
import os 

if __name__=="__main__":

    source_path = os.environ['HOME']+'/HW3/Dapp.sol'

    # w3=connectWeb3()
    # w3.miner.start(1)
    # time.sleep(4)

    deploy(source_path,w3)
    
# import sys
import time
# import pprint

from web3 import *
from solc import compile_source
import os
import sys 



from utils import deployContracts, connectWeb3



class Dapp:
    def __init__(self,source_path):
        self.w3=connectWeb3(),
        self.w3.miner.start(1)
        time.sleep(4)
        self.account=self.w3.eth.accounts[0]
        self.contract_interface, self.address = deployContracts(source_path=source_path,w3=self.w3, account=self.account)

        if self.address==-1:
            sys.exit("Deployment Unsuccessfull. Please reinitiate the process")

        self.contract=self.w3.eth.contract(address=self.address, abi=self.contract_interface['abi'])


    def __str__(self):
        curBlock=self.w3.getBlock('latest')
        print(curBlock)
    
    def exit(self):
        self.w3.miner.stop()
    
    def registerUser(self,uid, username):
        tx_hash=self.contract.functions.registerUser(uid,username).transact({'txType':"0x3", 'from':self.address, 'gas':3000000})
        time.sleep(0.01)
        receipt=self.w3.eth.getTransactionReceipt(tx_hash)
        while receipt is None:
            time.sleep(1)
            receipt=self.w3.eth.getTransactionReceipt(tx_hash)

        receipt=self.w3.eth.getTransactionReceipt(tx_hash)

        if receipt is not None:
            return receipt.status 
        
        return False

    
    def createAcc(self, uid1, uid2, val1, val2):
        tx_hash=self.contract.functions.createAcc(uid1, uid2, val1, val2).transact({'txType':"0x3", 'from':self.address, 'gas':3000000})
        time.sleep(0.01)
        receipt=self.w3.eth.getTransactionReceipt(tx_hash)
        while receipt is None:
            time.sleep(1)
            receipt=self.w3.eth.getTransactionReceipt(tx_hash)

        receipt=self.w3.eth.getTransactionReceipt(tx_hash)

        if receipt is not None:
            return receipt.status 
        
        return False

    def closeAccount(self, uid1, uid2):
        tx_hash=self.contract.functions.closeAccount(uid1, uid2).transact({'txType':"0x3", 'from':self.address, 'gas':3000000})
        time.sleep(0.01)
        receipt=self.w3.eth.getTransactionReceipt(tx_hash)
        while receipt is None:
            time.sleep(1)
            receipt=self.w3.eth.getTransactionReceipt(tx_hash)

        receipt=self.w3.eth.getTransactionReceipt(tx_hash)

        if receipt is not None:
            return receipt.status 
        
        return False
        
    
    def sendAmount(self, uid1, uid2, val):
        tx_hash=self.contract.functions.sendAmount(uid1, uid2, val).transact({'txType':"0x3", 'from':self.address, 'gas':3000000})
        time.sleep(0.01)
        receipt=self.w3.eth.getTransactionReceipt(tx_hash)
        while receipt is None:
            time.sleep(1)
            receipt=self.w3.eth.getTransactionReceipt(tx_hash)

        receipt=self.w3.eth.getTransactionReceipt(tx_hash)

        if receipt is not None:
            return receipt.status 
        
        return False



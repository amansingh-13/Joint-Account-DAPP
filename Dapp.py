# import sys
import time
# import pprint

# from web3 import *
from web3 import Web3
# from solcx import compile_source
# import os
import sys 
import web3 



from utils import deployContracts, connectWeb3
# from web3.exceptions import TransactionNotFound


class Dapp:
    def __init__(self,source_path):
        # print("Starting deploying contract")
        self.w3=connectWeb3()
        self.account=self.w3.eth.accounts[0]
        # print(self.account)
        # print("Waiting for 50 seconds")
        # time.sleep(40)
        print('Port connected')
        self.w3.geth.miner.start(1)
        time.sleep(4)
        print("Miner started")
        self.contract_interface, self.address = deployContracts(source_path=source_path,w3=self.w3, account=self.account)
        time.sleep(10)
        if self.address==-1:
            sys.exit("Deployment Unsuccessfull. Please reinitiate the process")

        self.contract=self.w3.eth.contract(address=self.address, abi=self.contract_interface['abi'])


    def __str__(self):
        curBlock=self.w3.getBlock('latest')
        print(curBlock)
    
    def exit(self):
        self.w3.geth.miner.stop()

    def check_alive(self) :
        tx_hash=self.contract.functions.alive().transact({'txType':"0x3", 'from':self.account, 'gas':3000000})
        time.sleep(0.01)
        receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash)
        while receipt is None:
            time.sleep(1)
            try:
                receipt=self.w3.eth.get_transaction_receipt(tx_hash)
            except web3.exceptions.TransactionNotFound:
                continue


        # receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt is not None:
            # print (receipt)
            # a=input()
            return True 
        
        return False

    def registerUser(self,uid, username):
        tx_hash=self.contract.functions.registerUser(uid,username).transact({'txType':"0x3", 'from':self.account, 'gas':3000000})
        time.sleep(0.01)
        receipt=None
        # receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash)
        while receipt is None:
            time.sleep(1)
            try:
                receipt=self.w3.eth.get_transaction_receipt(tx_hash)
            except web3.exceptions.TransactionNotFound:
                receipt=None
                

        # receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt is not None:
            return receipt
            # return (receipt['status']==1)
            # return receipt
        
        return False

    
    def bulk_user_reg(self, data):
        tx_hash=[]
        for user in data:
            th=self.contract.functions.registerUser(user[0],user[1]).transact({'txType':"0x3", 'from':self.account, 'gas':3000000})
            tx_hash.append(th)
        
        num_pending=len(tx_hash)
        num_txn=len(tx_hash)
        is_complete=[False]*num_txn

        while num_pending!=0:
            for i in range (num_txn):
                if not is_complete[i]:
                    receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash[i])
                    if receipt is not None :
                        num_pending-=1
                        is_complete[i]=True 
                        if (num_txn-num_pending)%10==0:
                            print (f'{num_txn-num_pending} users added')
            
                

        return True 
                    



    
    def createAcc(self, uid1, uid2, val1, val2):
        tx_hash=self.contract.functions.createAcc(uid1, uid2, val1, val2).transact({'txType':"0x3", 'from':self.account, 'gas':3000000})
        time.sleep(0.01)
        receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash)
        while receipt is None:
            time.sleep(1)
            receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash)

        receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt is not None:
            # return receipt.status 
            return True
        
        return False
    

    def bulk_create_acc(self, data):
        tx_hash=[]
        for a in data:
            th=self.contract.functions.createAcc(a[0], a[1], a[2], a[3]).transact({'txType':"0x3", 'from':self.account, 'gas':3000000})
            tx_hash.append(th)
        
        num_pending=len(tx_hash)
        num_txn=len(tx_hash)
        is_complete=[False]*num_txn

        while num_pending!=0:
            for i in range (num_txn):
                if not is_complete[i]:
                    receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash[i])
                    if receipt is not None :
                        num_pending-=1
                        is_complete[i]=True 
                        if (num_txn-num_pending)%20==0:
                            print (f'{num_txn-num_pending} edges added')
        
        # return True 


    def closeAccount(self, uid1, uid2):
        tx_hash=self.contract.functions.closeAccount(uid1, uid2).transact({'txType':"0x3", 'from':self.account, 'gas':3000000})
        time.sleep(0.01)
        receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash)
        # while receipt is None:
        #     time.sleep(1)
        #     receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash)

        # receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt is not None:
            return (receipt['status']==1)
            # return True
        
        return False
        
    
    def sendAmount(self, uid1, uid2, val):
        tx_hash=self.contract.functions.sendAmount(int(uid1), int(uid2), int(val)).transact({'txType':"0x3", 'from':self.account, 'gas':3000000})
        time.sleep(0.01)
        receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash)
        # while receipt is None:
        #     time.sleep(1)
        #     receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash)

        # receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt is not None:
            return (receipt['status']==1)
            # return True
        
        return False
    
    def bulk_sendAmount (self, data):
        tx_hash=[]
        for a in data:
            th=self.contract.functions.sendAmount(int(a[0]), int(a[1]), int(a[2])).transact({'txType':"0x3", 'from':self.account, 'gas':3000000})
            tx_hash.append(th)
        
        num_pending=len(tx_hash)
        num_txn=len(tx_hash)
        is_complete=[False]*num_txn
        num_successful=0

        # success_ratio=[]
        while num_pending!=0:
            # time.sleep(10)
            for i in range (num_txn):
                if not is_complete[i]:
                    receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash[i])
                    if receipt is not None :
                        if receipt['status']==1:
                            num_successful+=1
                        num_pending-=1
                        is_complete[i]=True 
                        #if (num_txn-num_pending)%100==99:
                        #    print (f'{num_txn-num_pending} transactions executed')
                        #    success_ratio.append(num_successful/(num_txn-num_pending))
        
        return num_successful 




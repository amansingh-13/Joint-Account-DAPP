import time
from web3 import Web3

import sys 
import web3 



from utils import deployContracts, connectWeb3

# Dapp class to compile and deploy a dapp and provide a interface to 
# interact with the contract
class Dapp:
    def __init__(self,source_path):
        self.w3=connectWeb3() # connecting to the network 
        self.account=self.w3.eth.accounts[0] # address of node from which contract is deployed
        print('[*] Connected to the network')
        self.w3.geth.miner.start(1) #starting miner
        time.sleep(4)
        print("[*] Miner started")
        self.contract_interface, self.address = deployContracts(source_path=source_path,w3=self.w3, account=self.account) # contract interface and address of contract
        time.sleep(10)
        
        #checking whether contract deployment was successfull or not 
        if self.address==-1:
            sys.exit("Deployment Unsuccessfull. Please reinitiate the process")

        self.contract=self.w3.eth.contract(address=self.address, abi=self.contract_interface['abi'])


    def __str__(self):
        curBlock=self.w3.getBlock('latest')
        print(curBlock)

    # this function should be called at the end 
    def exit(self):
        self.w3.geth.miner.stop()

    # dummy function to check if contract was successfully deployed
    def check_alive(self) :
        tx_hash=self.contract.functions.alive().transact({'txType':"0x3", 'from':self.account, 'gas':1000000000})
        time.sleep(0.01)
        receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash)
        while receipt is None:
            time.sleep(1)
            try:
                receipt=self.w3.eth.get_transaction_receipt(tx_hash)
            except web3.exceptions.TransactionNotFound:
                continue

        if receipt is not None:
            return True 
        
        return False

    # function to register one new user 
    def registerUser(self,uid, username):
        tx_hash=self.contract.functions.registerUser(uid,username).transact({'txType':"0x3", 'from':self.account, 'gas':1000000000})
        time.sleep(0.01)
        receipt=None
        
        while receipt is None:
            time.sleep(1)
            try:
                receipt=self.w3.eth.get_transaction_receipt(tx_hash)
            except web3.exceptions.TransactionNotFound:
                receipt=None

        if receipt is not None:
            return (receipt['status']==1)
        
        return False

    
    # function to register large amount of user. 
    # this function saves a lot of time 
    # by sending a stream of regUser txn without waiting each of them to complete 
    # and finally wait for each of them before returning 
    def bulk_user_reg(self, data):
        tx_hash=[]
        for user in data:
            th=self.contract.functions.registerUser(user[0],user[1]).transact({'txType':"0x3", 'from':self.account, 'gas':1000000000})
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
                    



    # function ot create a joint account between to user 
    def createAcc(self, uid1, uid2, val1, val2):
        tx_hash=self.contract.functions.createAcc(uid1, uid2, val1, val2).transact({'txType':"0x3", 'from':self.account, 'gas':1000000000})
        time.sleep(0.01)
        receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash)
        while receipt is None:
            time.sleep(1)
            receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash)

        receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt is not None:
            return (receipt['status']==1)

        return False
    
    # function to create joint account between multiple user.
    # this function saves a lot of time 
    # by sending a stream of createAcc txn without waiting each of them to complete 
    # and finally wait for each of them before returning 
    def bulk_create_acc(self, data):
        tx_hash=[]
        for a in data:
            th=self.contract.functions.createAcc(a[0], a[1], a[2], a[3]).transact({'txType':"0x3", 'from':self.account, 'gas':1000000000})
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
        
        

    #function to close account between two user 
    def closeAccount(self, uid1, uid2):
        tx_hash=self.contract.functions.closeAccount(uid1, uid2).transact({'txType':"0x3", 'from':self.account, 'gas':1000000000})
        time.sleep(0.01)
        receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if receipt is not None:
            return (receipt['status']==1)
        
        
        return False
        
    # function to send some amount from one user to another
    def sendAmount(self, uid1, uid2, val):
        tx_hash=self.contract.functions.sendAmount(int(uid1), int(uid2), int(val)).transact({'txType':"0x3", 'from':self.account, 'gas':1000000000})
        time.sleep(0.01)
        receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if receipt is not None:
            return (receipt['status']==1)
        
        return False
    
    # function to send a bulk txn request.
    # This function return the number of suuccessfull request.
    # This function is used to make the simulation more realistic as in real world one txn doesn't wait for other to complete.
    # This also saves a lot of time 
    def bulk_sendAmount (self, data):
        tx_hash=[]
        for a in data:
            th=self.contract.functions.sendAmount(int(a[0]), int(a[1]), int(a[2])).transact({'txType':"0x3", 'from':self.account, 'gas':1000000000})
            tx_hash.append(th)
        
        num_pending=len(tx_hash)
        num_txn=len(tx_hash)
        is_complete=[False]*num_txn
        num_successful=0

        while num_pending!=0:
            for i in range (num_txn):
                if not is_complete[i]:
                    receipt=self.w3.eth.wait_for_transaction_receipt(tx_hash[i])
                    if receipt is not None :
                        if receipt['status']==1:
                            num_successful+=1
                        num_pending-=1
                        is_complete[i]=True 
                       
        return num_successful 




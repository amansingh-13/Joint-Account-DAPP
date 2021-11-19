import time
# import pprint

from web3 import Web3
from solc import compile_source
import os

def connectWeb3():
    # print(os.environ['HOME']+'/HW3/test-eth1/geth.ipc')
    return Web3(Web3.IPCProvider(os.environ['HOME']+'/HW3/test-eth1/geth.ipc', timeout=100000))

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)



def deployEmptyContract(source_path, w3, account):
    # compiled_sol = compile_source_file(contract_source_path)
    compiled_sol = compile_source_file(source_path)
    contract_id, contract_interface3 = compiled_sol.popitem()
    if contract_id=="<stdin>:Queue":
        contract_id, contract_interface3 = compiled_sol.popitem()
    assert(contract_id=="<stdin>:Dapp")
    # contract_interface3=get_interface(source_path=source_path)
    # curBlock = w3.eth.getBlock('latest')
    tx_hash = w3.eth.contract(
            abi=contract_interface3['abi'],
            bytecode=contract_interface3['bin']).constructor().transact({'txType':"0x0", 'from':account, 'gas':1000000})
    
    return tx_hash, contract_interface3


def deployContracts(source_path,w3, account):
    tx_hash3, contract_interface = deployEmptyContract(source_path, w3, account)

    
    
    receipt3 = w3.eth.wait_for_transaction_receipt(tx_hash3)

    while ((receipt3 is None)) :
        time.sleep(1)
        receipt3 = w3.eth.wait_for_transaction_receipt(tx_hash3)

    # w3.miner.stop()
    # receipt3 = w3.eth.wait_for_transaction_receipt(tx_hash3)
    
    if receipt3 is not None:
        # f=open("contractAddressList","w")
        # print("empty:{0}".format(receipt3['contractAddress']), file=f)
        # f.close() 
        print("Contract Deployed")
        return contract_interface,receipt3['contractAddress']
    
    return None,-1
    
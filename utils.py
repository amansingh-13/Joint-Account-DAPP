import time
from web3 import Web3
from solcx import compile_source
import os

# attach to ipc file
def connectWeb3():
    return Web3(Web3.IPCProvider('../HW3/test-eth1/geth.ipc', timeout=100000))

#compile the given solidity file
def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source=source, solc_binary="../HW3/solc")


# send the deploy contarct request and return the txn_hash.
# it doesn't wait for the contract to be successfully deployed
# This is  a helper function for deploying contracts 
def deployEmptyContract(source_path, w3, account):
    
    compiled_sol = compile_source_file(source_path)
    contract_id, contract_interface3 = compiled_sol.popitem()
    if contract_id=="<stdin>:Queue":
        contract_id, contract_interface3 = compiled_sol.popitem()
    assert(contract_id=="<stdin>:Dapp")
    
    tx_hash = w3.eth.contract(
            abi=contract_interface3['abi'],
            bytecode=contract_interface3['bin']).constructor().transact({'txType':"0x0", 'from':account, 'gas':1000000000})
    
    return tx_hash, contract_interface3

# This function is used to deploy the contract with the help of above function.
# It waits for the contract to be successfully deployed
# Return the address of the deployed contract
# Upon unsuccessfull deployment return -1 as the contract address 
def deployContracts(source_path,w3, account):
    tx_hash3, contract_interface = deployEmptyContract(source_path, w3, account)
    receipt3 = w3.eth.wait_for_transaction_receipt(tx_hash3) # blocking function. Wait for txn to complete (max wait time = 120s)

    while ((receipt3 is None)) :
        time.sleep(1)
        receipt3 = w3.eth.wait_for_transaction_receipt(tx_hash3)

    if receipt3 is not None:
        print("[*] Contract Deployed")
        return contract_interface,receipt3['contractAddress']
    
    return None,-1
    

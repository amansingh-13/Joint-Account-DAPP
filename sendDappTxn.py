import sys
import time
import pprint

from web3 import *
from solcx import compile_source
import os

w3=None 

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)

def sendTxn(address):
    ...



def registerUser():
    ...





def sendEmptyLoopTransaction(source_path,address):
       
    # contract_source_path = os.environ['HOME']+'/HW3/emptyLoop.sol'
    compiled_sol = compile_source_file(source_path)

    contract_id, contract_interface = compiled_sol.popitem()

    sort_contract = w3.eth.contract(
    address=address,
    abi=contract_interface['abi'])
    tx_hash = sort_contract.functions.runLoop().transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409638})
    return tx_hash



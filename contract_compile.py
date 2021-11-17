import time
# import pprint

from web3 import *
from solc import compile_source
import os

def connectWeb3():
    # print(os.environ['HOME']+'/HW3/test-eth1/geth.ipc')
    return Web3(IPCProvider(os.environ['HOME']+'/HW3/test-eth1/geth.ipc', timeout=100000))

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)

def get_interface(source_path):
    compiled_sol = compile_source_file(contract_source_path)

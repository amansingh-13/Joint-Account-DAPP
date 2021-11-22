from web3 import Web3
import time 
import numpy as np
import networkx as nx
import os 
import sys 
import matplotlib.pyplot as plt

from Dapp import Dapp
NUM_NODES = 100

# generates a scale free network as described here : 
# https://en.wikipedia.org/wiki/Barab%C3%A1si%E2%80%93Albert_model

def generate_network(n_nodes):
    G = nx.erdos_renyi_graph(10, 0.5, directed=False, seed=13)
    for i in range(10,n_nodes):
        denom =  sum(dict(G.degree).values())
        for j in range(i):
            if(np.random.random() < G.degree[j]/denom):
                G.add_edge(i, j)
        # if node i could not connect to any other node
        try: G.degree[i]
        except: G.add_edge(i, np.random.randint(i))
    return G

if __name__ == "__main__":

    # deploy the Dapp    
    source_path = './Dapp.sol'
    dapp = Dapp(source_path)

    alive = dapp.check_alive()
    if not alive:
        sys.exit("[ERR] Contract not alive")

    # register users to the network

    print ("[ ] Registering Users...")
    user_data=[]
    for i in range(NUM_NODES):
        user_data.append((i, 'user_'+str(i)))
    dapp.bulk_user_reg(user_data)
    print ("[*] Users Registered")

    # create joint accounts based on the scale-free network model
    # initialise the account with balance from a exponential 
    # distribution of mean 10, divided equally

    print ("[ ] Generating a connected network...")
    G = generate_network(NUM_NODES)
    edge_data=[]
    for i,j in G.edges:
        indv_amnt = int(np.random.exponential(10) / 2)
        edge_data.append((i, j, indv_amnt, indv_amnt))
    dapp.bulk_create_acc(edge_data)
    print ("[*] Network created")

    # Release transactions 25 at a time, wait for their 
    # confirmation/rejection and collect required statistics

    print ("[ ] Sending Transaction Stream....")
    to_graph = []
    success  = 0  
    txn_data = []
    for txn in range(1000):
        x, y = np.random.choice(NUM_NODES, 2, replace=False)
        txn_data.append((x, y, 1))

        if((txn+1)%25 == 0):
            success += dapp.bulk_sendAmount(txn_data)
            txn_data = []
            print (f"Txns generated : {txn+1}, Successful Txns : {success}")        
            if((txn+1)%100 == 0):
                to_graph.append(success / (txn+1))

    # stop the miner
    dapp.exit()

    # print results and draw the graph
    print ("Ratio of successful txns (after every 100 txns) :", to_graph)
    plt.plot(range(100,1000+1,100), to_graph)
    plt.xlabel('Number of transactions')
    plt.ylabel('Success rate of transactions')
    plt.show()
    

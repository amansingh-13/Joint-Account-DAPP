from web3 import *
import time 
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from Dapp import Dapp
from contract_compile import connectWeb3

NUM_NODES = 100

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

if __name__=="__main__":

    source_path = os.environ['HOME']+'/HW3/Dapp.sol'

    dapp = Dapp(source_path)

    for i in range(NUM_NODES):
        dapp.registerUser(i, 'user_'+str(i))

    G = generate_network(NUM_NODES)
    for i,j in G.edges:
        indv_amnt = int(np.random.exponential(10) / 2)
        dapp.createAcc(i, j, indv_amnt, indv_amnt)
    
    to_graph = []
    success = 0    
    for txn in range(1000):
        x, y = np.random.choice(NUM_NODES, 2, replace=False)
        success += dapp.sendAmount(x, y, 1)

        if((txn+1) % 100 == 0):
            to_graph.append(success / (txn+1))

    plt.plot(range(100,1000+1,100), to_graph)
    plt.xlabel('xlabel', 'Number of transactions')
    plt.ylabel('ylabel', 'Success rate of transactions')
    plt.show()
    
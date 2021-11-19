from web3 import *
import time 
import numpy as np
import networkx as nx
import os 
import sys 
# import matplotlib.pyplot as plt

from Dapp import Dapp
# from contract_compile import connectWeb3

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

    alive= dapp.check_alive()

    if not alive:
        sys.exit("Contract not alive")

    print ("Registering Users...")

    user_data=[]

    # for i in range(NUM_NODES):
    #     dapp.registerUser(i, 'user_'+str(i))
    #     if (i%10==9):
    #         print (f"{i+1} users registered")
    for i in range(NUM_NODES):
        user_data.append((i, 'user_'+str(i)))
    dapp.bulk_user_reg(user_data)
    
    print ("Users Registered")
    print ("Generating a connected network...")
    G = generate_network(NUM_NODES)

    numEdges=len(G.edges)
    # edgesAdded=0
    edge_data=[]
    for i,j in G.edges:
        indv_amnt = int(np.random.exponential(10) / 2)
        # dapp.createAcc(i, j, indv_amnt, indv_amnt)
        edge_data.append((i, j, indv_amnt, indv_amnt))
        # edgesAdded+=1
        # if (edgesAdded%10==0):
            # print (f"{edgesAdded} edges added")
    
    dapp.bulk_create_acc(edge_data)

    print ("Network created")
    print("Sending Transaction Stream")
    to_graph = []
    success = 0    
    for txn in range(1000):
        x, y = np.random.choice(NUM_NODES, 2, replace=False)
        success += dapp.sendAmount(x, y, 1)

        if((txn+1) % 100 == 0):
            to_graph.append(success / (txn+1))
            print (f"{txn}:")
            print (to_graph)
    print ("final results")
    print (to_graph)
    dapp.exit()
    # plt.plot(range(100,1000+1,100), to_graph)
    # plt.xlabel('xlabel', 'Number of transactions')
    # plt.ylabel('ylabel', 'Success rate of transactions')
    # plt.show()
    
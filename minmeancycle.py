from __future__ import division
import networkx as nx
import numpy as np
import csv

def MinMeanCycle(G):

    n = G.number_of_nodes()
    d = [[0 for j in range(n)] for k in range(n+1)]


    # d[k][j] is the cost of the min-cost path from dummy source s to 
    # node j using exactly k+1 arcs
    
    for k in range(1,n+1):
        for j in G.nodes():
            d[k][j] = float('inf')
            for i in G.predecessors(j):
                temp = d[k-1][i] + G[i][j]['cost']
                if temp < d[k][j]:
                    d[k][j] = temp
                    
    print(d)
                                       

    # ratio[j] is the minimum over k of (d[k][j]-d[n][j])/(n-k)
    ratio = [float('inf') for j in range(n)]
    for j in G.nodes():
        for k in range(0,n):
            temp = (d[k][j]-d[n][j])/(n-k)
            if temp < ratio[j] :
                ratio[j] = temp
               
    # |mu| is the maximum of ratio[j] over all j              
    absmu = max(ratio)
    #find j*
    js = np.argmax(ratio)
    W = [js]
    k = n
 
 #backtrack
    while k > 0:
        for i in G.predecessors(j):
            if d[k-1][i] == d[k][j] - G[i][j]['cost']:
                if i in W:
                    mu = -absmu
                    return[mu, list(reversed(W[W.index(i):]))]       
                W.append(i)

        j = i
        k -= 1
            
        #print(v)
    
    #W.reverse()

    # To find W, find j* that gave the maximum ratio, and backtrack to 
    # find the path of n arcs that gave the value d[n][j*]
    # Any cycle on this path can be taken as W
    
    # YOUR CODE HERE

def read_into_graph(inputfile) :   
     with open(inputfile) as f:
        data = [list(map(int,row)) for row in csv.reader(f, delimiter = ' ')]
     
     G = nx.DiGraph()
     for i in range(len(data)):
         G.add_edge(data[i][0], data[i][1], cost = data[i][2])
     return G
 

G = read_into_graph('ncycle0.txt')
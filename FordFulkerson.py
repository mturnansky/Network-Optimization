#ford fulkerson implentation

import networkx as nx
import csv

#read data into graph structure
def read_into_graph(inputfile) :   
     with open(inputfile) as f:
        data = [list(map(int,row)) for row in csv.reader(f, delimiter = ',')]
     
     G = nx.DiGraph()
     for i in range(len(data)):
         G.add_edge(data[i][0],data[i][1],{'u' : data[i][2], 'x' : data[i][3]})
     return G

def find_augmenting_path(G, s, t):
    # returns an augmenting path P and its capacity Delta
    # if there is no augmenting path, Delta is 0 and P contains S*, the s-side of a minimum s-t cut
    marked = set()
    marked.add(s)
    pred = {}
    pred[s] = 0
    LIST = [s]
    while LIST:
        i = LIST[0]
        # scan forward arcs out of i
        for j in G.successors(i):
             if j not in marked and j not in LIST and G[i][j]['u'] - G[i][j]['x'] > 0:
                
                  pred[j] = i
                  LIST.append(j)

        # scan backward arcs out of i                
        for j in G.predecessors(i):
             if j not in marked and j not in LIST and G[j][i]['x'] > 0:
                  pred[j] = i
                  LIST.append(j)
            
        
        LIST.pop(0) 
        marked.add(i)
#find Delta
    if t not in marked :
        P = marked
        Delta = 0
    else:
        cur = t
        P = [cur]
        Delta = float('inf')
        while P[-1] != s:
            prev = cur
            cur = pred[prev]
            P.append(cur)
            if G.has_edge(cur, prev):
                r = G[cur][prev]['u'] - G[cur][prev]['x']
            else:
                r = G[prev][cur]['x']
            Delta = min(Delta, r)                    
        P.reverse()
    return [Delta, P]                
                    
def max_flow(G,s,t):
    """G is a directed graph with s,t nodes in G. Each arc in G has an attribute G[i][j]['u'] 
    indicating its capacity and may have an attribute G[i][j]['x'] indicating its current flow"""

    for (i,j) in G.edges():
        try :
            uij = G[i][j]['u']
        except :
            uij = float.inf()
            G[i][j]['u'] = uij
        try :
            xij = G[i][j]['x']
        except :
            xij = 0
            G[i][j]['x'] = xij            

    updated = True            
    while updated :
        updated = False
        [Delta, P ] = find_augmenting_path(G,s,t)                  
        if Delta > 0 :
          for j in range(0,len(P) - 1):
               if G.has_edge(P[j], P[j+1]):
                    G[P[j]][P[j+1]]['x'] = G[P[j]][P[j+1]]['x'] + Delta
                    
               else:
                    G[P[j+1]][P[j]]['x'] = G[P[j+1]][P[j]]['x']  - Delta
                
          updated = True
    
    return G, P            

#test code
#G = nx.DiGraph()
#G.add_edges_from([(1,2,{'u':8,'x':6}),(1,4,{'u': 9,'x':5}),(2,3,{'u':4,'x':2}),(2,5,{'u':5,'x':5}),(3,6,{'u':6,'x':5}), (4,3,{'u': 3,'x':3}), (4,5,{'u':2,'x':1}),(4,2,{'u':1,'x':1}), (5,3,{'u':2,'x': 0}), (5,6,{'u':10,'x':6}), (6,5,{'u':10,'x':0})])

#G2 = max_flow(G, 1, 6)[0]
#G2[1][4]['u'] = 6
#G2[4][5]['u'] = 3


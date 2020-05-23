#run in python 2 the division in python truncates instead of converts to float
#othwerwise it won't work as written
import networkx as nx
import csv

def read_into_graph(inputfile) :   
     with open(inputfile) as f:
        data = [list(map(int,row)) for row in csv.reader(f, delimiter = ',')]
     
     G = nx.DiGraph()
     for i in range(len(data)):
         G.add_edge(data[i][0],data[i][1],{'u' : data[i][2], 'x' : data[i][3]})
     return G

def find_augmenting_path(G, s, t, phase):
    # returns an augmenting path P and its capacity Delta
    # if there is no augmenting path, Delta is 0 and P contains S*, the s-side of a minimum s-t cut
    marked = set()
    marked.add(s)
    pred = {}
    pred[s] = 0
    LIST = [s]
    while LIST:
        i = LIST[0]
        # scan forward arcs out of i with capacity >= phase
        for j in G.successors(i):
             if j not in marked and j not in LIST and G[i][j]['u'] - G[i][j]['x'] >= phase:
                  pred[j] = i
                  LIST.append(j)

        # scan backward arcs out of i with capacity >= phase               
        for j in G.predecessors(i):
             if j not in marked and j not in LIST and G[j][i]['x'] >= phase:
                  pred[j] = i
                  LIST.append(j)
                 
        LIST.pop(0) 
        marked.add(i)

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
    # G is a directed graph with s,t nodes in G. Each arc in G has an attribute G[i][j]['u'] indicating its capacity and may have an attribute G[i][j]['x'] indicating its current flow

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
     
    #find the max edge capacity
    U = nx.get_edge_attributes(G,'u')
    U = max(U)
    U = G[U[0]][U[1]]['u']  
     
    #find the initial phase
    phase = U
    while phase != 0:
        Delta, P  = find_augmenting_path(G,s,t, phase)                  
        if Delta > 0:
          for j in range(0,len(P) - 1):
               if G.has_edge(P[j], P[j+1]):
                    G[P[j]][P[j+1]]['x'] = G[P[j]][P[j+1]]['x'] + Delta
                    
               else:
                    G[P[j+1]][P[j]]['x'] = G[P[j+1]][P[j]]['x']  - Delta
        else:
             phase = phase / 2


    return G, P            

#test code
# G = nx.DiGraph()
# G.add_edges_from([(1,2,{'u':8,'x':0}),(1,4,{'u': 9,'x':0}),(2,3,{'u':4,'x':0}),(2,5,{'u':5,'x':0}),(3,6,{'u':6,'x':0}), (4,3,{'u': 3,'x':0}), (4,5,{'u':2,'x':0}),(4,2,{'u':1,'x':0}), (5,3,{'u':2,'x': 0}), (5,6,{'u':10,'x':0}), (6,5,{'u':10,'x':0})])


# print(max_flow(G, 1, 6)[1])
# G[1][4]['u'] = 6
# G[4][5]['u'] = 3

#print(max_flow(G,1,6)[1])

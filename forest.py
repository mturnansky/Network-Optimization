#Find if a graph is a random forest


import networkx as nx
from GraphSearch import *

#check to see if a given graph is acyclic
def Forest(G):
#check
    H = G.to_undirected()
    if G.number_of_edges() != H.number_of_edges():
        return(False)
    
#check to see if the undirected graph of G has any cycles
    nodes = H.nodes()
#evaluate each component until either a cycle is found or all components are checked
    while(G.nodes()):
#generate components starting in unexplored vertex
        H = G.subgraph(GraphSearch(G, nodes[0],0)[0])
#if a connected undirected graph has more than n - 1 edges it has a cycle
        if H.number_of_edges() >  H.number_of_nodes() - 1:
            return(False)
        else:
        #remove all nodes in the component containing node[0] and update nodes
            for element in H.nodes():
                G.remove_node(element)
        
#all possibilities have been checked, so the graph must be a forest
    return(True)

def GraphSearch(G, s, order = 0):
    # order is 0 if we want to search in BFS order, and 1 if we want to search in DFS order  
    # default is to run BFS starting from the first node in G  
    s = next(G.nodes_iter())
    marked = []
    marked.append(s)
    pred = {}
    pred[s] = 0
    LIST = [[s, G.neighbors_iter(s)]]  # rather than only adding s, we also create an "iterator" for scanning through its neighbors. 
    # Each time you call next() for this iterator, it returns the next neighbor we did not yet scan.

    while LIST :
        # take an element from the LIST (either first or last depending on 'order')
        [i,neighbors] = LIST[-order]
        
        
        try :
            # take the next neighbor of i and check if (i,j) is admissible
            j = next(neighbors)
            if j not in marked :
                marked.append(j)
                pred[j] = i
                LIST.append([j,G.neighbors_iter(j)])    
                
        except :
            # if all arcs out of i have been scanned, remove i
            LIST.pop(-order)

    return  (marked,pred)



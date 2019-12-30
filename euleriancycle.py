#Find the eulerian cycle in each componenent of a graph

import networkx as nx

def Eulerian_cycle_for_each_component(G):
#check to see if graph is directed or undirected
    if nx.is_directed(G):
#verify that the in degree equals the out degree for each vertex
        for element in G.__iter__():
            if G.in_degree(element) != G.out_degree(element):
                print("The in degree of all nodes must equal the out degree")
                return()

#if conditions are met, find directed Eulerian cycle for each component        
        for element in nx.weakly_connected_component_subgraphs(G):
            Eulerian_cycle(element)
    else:
#if conditions are met, find undirected Eulerian cycle for each component
        for element in nx.connected_component_subgraphs(G):
            Eulerian_cycle(element)

def Eulerian_cycle(G):

    u = next(G.nodes_iter()) # Take the first node in G 
    F = G.copy()    # F contains the edges not yet used in T
    T = [u]         # T is an Eulerian cycle of the graph containing the edges in G that are not in F

    while (F.edges()) :

        try :
            (v,w) = next(F.edges_iter(T)) # gives an error if there are no edges in F incident to T
            q = T.index(v)
            C = find_closed_walk(v,F) 
            if C == False:
                return False
            else :
                print("Inserting cycle ", C, " in position ", q, " of ", T)
                T = T[0:q] + C + T[q+1:len(T)]
                print("New T is ", T)                      
        except :    
            print("The nodes of degree > 0 have to be connected")
            return False
    return T                

def find_closed_walk(v,F) :
# returns a closed walk C in F starting and ending in node v
# the edges in C are removed from F    
    prev = v
    curr = next(F.neighbors_iter(v))
    C = [prev,curr]
    F.remove_edge(prev,curr)
    while v != curr :
        try :
            prev = curr
            curr = next(F.neighbors_iter(prev))
            C.append(curr)
            F.remove_edge(prev, curr)
        except :
            print("The nodes must all have even degree")
            return False
    return C                

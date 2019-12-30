import networkx as nx

#test shortest path with simple examples
G = nx.DiGraph()
G.add_edges_from([(1,2,{'cost':-2}),(2,4,{'cost':3}),(4,3,{'cost':-1}),(3,2,{'cost':-1}),(4,5,{'cost':5})])

G2 = nx.DiGraph()
G2.add_edges_from([(1,2,{'cost':2}),(2,4,{'cost':3}),(4,3,{'cost':-1}),(3,2,{'cost':-4}),(4,5,{'cost':5})])


#find the shortest path between the source node and all other nodes
def ShortestPath(G, s = G.nodes()):

    d = {}
    pred = {}
    for i in list(G.nodes()):
        d[i] = float('inf')
    d[s] = 0
    pred[s] = -1
    updated = True
    counter = 0
    lastupdated = [s]
    while updated and counter < G.number_of_nodes():
        counter += 1
        updated = False
        for (i,j) in G.successors(lastupdated[-1])[s]:
            cij = G[i][j]['cost']
            if d[j] > d[i] + cij :
                d[j] = d[i] + cij
                pred[j] = i
                updated = True
                lastupdated.append(j)
            lastupdated = lastupdated[1,-1]
   
#use counter to avoid infinite loop when a negative cycle occurs         
    if counter == G.number_of_nodes() and updated :
        print("G has a negative cycle")
        print("Find the negative cycle by backtracking the predecessor arcs starting from", lastupdated)                
    return (d, pred, counter, lastupdated)                
                
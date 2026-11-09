import networkx as nx #This line imports the library that creates and solves graphs

#Informations about the Knapsack Problem at the Graph Form:
n = 4 #The numbers of variables
weight = [1,1,2,3] #The weights of variables that occupy in the bag
value = [2,3,2,5] #The values of variables in Objective Function
capacity = 3 #The bag's capacity

#Modeling of Problem
# Node (i, r): the item i is about to be decided and r is the remaining capacity of the bag
# Start node: (0, capacity)
# Arc "not put": (i, r) -> (i+1, r), with weight 0
# Arc "put":     (i, r) -> (i+1, r - weight[i]), with weight value[i]
#                (this arc only exists if r >= weight[i])
# Final node T: every node of the last layer (n, r) is connected to T, with weight 0
# Solution: the longest path (in total weight) from (0, capacity) to T
# The total weight of this path is the optimal value,
# and the items chosen are the ones whose arcs in the path are of the type "put"

G = nx.DiGraph() #This line creates an empty directed graph, because the arcs always go from item i to item i+1
layer = {capacity} #This line creates the layer 0, a set with the possible remaining capacities: {3}
for i in range(n): #This line makes one loop for each item, and each loop builds the next layer
    news = set() #This line creates the empty set of the next layer (a set does not repeat nodes)
    for r in layer: #This line goes through each remaining capacity possible in the current layer
        G.add_edge((i,r), (i+1,r), weight = 0, put = False) #This line creates the arc "not put": the capacity does not change and the gain is 0
        news.add(r) #This line saves the capacity r as a node of the next layer
        if r >= weight[i]: #This line checks if the item i fits in the bag
            G.add_edge((i,r), (i+1,r-weight[i]), weight = value[i], put = True) #This line creates the arc "put": the capacity decreases and the gain is value[i]
            news.add(r-weight[i]) #This line saves the new capacity as a node of the next layer
    layer = news #This line makes the new layer be the current layer for the next loop

for r in layer: #Here layer is already the last layer (n), so this line goes through its nodes
    G.add_edge((n,r), "T", weight = 0, put = False) #This line connects each node of the last layer to the final node T

walk = nx.dag_longest_path(G, weight = "weight") #This line finds the longest path of the graph (it can end before T, but the value and the items are the same)
total_value = nx.dag_longest_path_length(G, weight = "weight") #This line gives the total weight of this path, that is the optimal value

#Output of Problem
chosen = [] #This line creates the list of items that are put in the bag
for u,v in zip(walk, walk[1:]): #This line goes through the pairs of neighbor nodes of the path, that are the arcs used
    if v != "T" and G[u][v]["put"]: #This line checks if this arc is of the type "put"
        chosen += [u[0]] #This line saves the item, because u[0] is the index i of the node (i, r)
print(f'This Optimal value of problem is {total_value} and chosen variables are x{chosen}') #This line shows the result

import gurobipy as gb
from gurobipy import GRB
import networkx as nx

#Data
n = 5 #Nodes 0..4
e = [1,0,0,0,0] #e[i] = 1: one unit enters the netwoek at node 0 (source)
s = [0,0,0,1,0] #s[i] = 1: one unit leaves the network at node 3 (sink)
cost = {(i,j): abs(j-i) for i in range(n) for j in range(n) if i != j} #cost[i,j] = |j-i|, only for i != j
cap = 1 #Capacity shared by each pair of nodes 

#Modeling of Problem
#Directed graph: node attributes e (enters) and s (leaves); edge attributes f (capacity) and c (cost)
#Same model as above, but the sums run over DG.in_edges(v) and DG.out_edges

#Creating Graph
DG = nx.DiGraph()
DG.add_nodes_from([(i,{'e':e[i],'s':s[i]}) for i in range(n)])
for i in DG.nodes():
    for j in DG.nodes():
        if i != j:
            DG.add_edge(i,j,f=cap,c=cost[i,j]) #Complete directed graph: every ordered pair has an edge

#Creating Model
mcfp_graph = gb.Model("Minimum Cost Flow Problem at Graph form")
x = {}
for i,j,d in DG.edges(data=True):
    x[i,j] = mcfp_graph.addVar(vtype=GRB.CONTINUOUS,name=f"x{i}{j}") #One flow variable for eacher edge of the graph

#in - out = s - e: the source sends one unit more than it receives, the sink receives one unit more than it sends
for v,d in DG.nodes(data=True): #d is the node dictionary: {'e':..., 's':...}
    mcfp_graph.addConstr(gb.quicksum(x[u,v] for (u,v) in DG.in_edges(v))  #Edges that enter v
                          - gb.quicksum(x[v,u] for (v,u) in DG.out_edges(v))  #minus edges that leave v
                          == d['s'] - d['e']) #-1 at the source, +1 at the sink, 0 otherwise

for i,j,d in DG.edges(data=True): #d is the edge dictionary: {'f': ..., 'c': ...}
    if i < j: #Each pair once, because DG has both i -> j and j -> i
        mcfp_graph.addConstr(x[i,j] + x[j,i] <= d['f']) #Capacity f shared by the two directions

mcfp_graph.setObjective(gb.quicksum(d['c']*x[i,j] for i,j,d in DG.edges(data=True)),GRB.MINIMIZE) #Total cost = sum of cost * flow of each edge
mcfp_graph.optimize() #To solve Minimum Cost Flow Problem 

#Output 
if mcfp_graph.status == GRB.OPTIMAL:
    print(f'The Optimal Value is {mcfp_graph.ObjVal}')
    for (i,j) in x:
        if x[i,j].X > 1e-6:
            print(f'x{i}{j} = {x[i,j].X}')
import gurobipy as gb
from gurobipy import GRB
import networkx as nx

#Costs
c = [[1,2,2,1],
     [0,3,2,1],
     [2,1,0,2],
     [1,0,3,3]]

# Matrix's dimension 
n = len(c[0])
for i in range(n):
    print(c[i],'\n')

#Creating model
model = gb.Model('Problem')

x = {} #Create empty dictionary

#Creating variables
for i in range(n):
    for j in range(n):
        x[(i,j)] = model.addVar(vtype=GRB.BINARY,name=f"x{i}{j}")

#Creating restrictions       
for i in range(n):
    model.addConstr(gb.quicksum(x[(i,j)] for j in range(n)) == 1)

#Creating restrictions  
for j in range(n):
    model.addConstr(gb.quicksum(x[(i,j)] for i in range(n)) == 1)

#Creating Objective Function
model.setObjective(gb.quicksum(c[i][j]*x[(i,j)] for i in range(n) for j in range(n)),GRB.MAXIMIZE)

#To solve ILPP
model.optimize()

#Checking the Optime value
if model.status == GRB.OPTIMAL:
    print(f'Optimal objective Value: {model.ObjVal}')
    for i in range(n):
        for j in range(n):
            print(f'x{i}{j} = {x[(i,j)].X}')

def e(i,j): #To peform
    return(min(i,j),max(i,j))

G = nx.Graph() #Creating Graph
G.add_node(0) #Add node
G.add_node(1) #Add node
G.add_edge(0,1) #Add edge
G.add_nodes_from([1,3,5]) #Add nodes from list
G.add_edges_from([e(1,3),e(5,3)]) #Add edges from list
print(G.nodes()) #Print nodes
print(G.edges()) #Print edges

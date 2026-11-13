import gurobipy as gb
from gurobipy import GRB
import networkx as nx

def e(i,j):
    return(min(i,j),max(i,j))

#Costs
c = [[1,2,2,1],
     [0,3,2,1],
     [2,1,0,2],
     [1,0,3,3]]

n = len(c[0])  #Dimension, obs one person to one task

G = nx.Graph() #Creating Graph

for i in range(n):
    G.add_node(i,label='people') #add Node on Graph

for j in range(n,n*2):
    G.add_node(j,label='tasks') #add Node on Graph

print(G.nodes(data=True)) #Print nodes

for i,j in G.nodes(data=True): # Person dictionary
    if (j['label'] == 'people'):
        print(f'Person {i}')

for i,j in G.nodes(data=True): # Task dictionary
    if (j['label'] == 'tasks'):
        print(f'Task {i}')

for i in range(n): # Contect tasks with people 
    for j in range(n,2*n):
        G.add_edge(i,j,cost=c[i][j-n])

print(G.edges(data=True))

#Creating model
model = gb.Model('Problem')

x = {} #Create empty dictionary

#Creating variables
for i,j,d in G.edges(data=True):
    x[e(i,j)] = model.addVar(vtype=GRB.BINARY,name=f"x{i}{j}") 

#Creating restrictions 
for i in G.nodes():
    model.addConstr(gb.quicksum(x[e(i,j)] for i,j in G.edges(i)) == 1)

#Creating Objective Function
model.setObjective(gb.quicksum(d['cost']*x[e(i,j)] for i,j,d in G.edges(data=True)),GRB.MAXIMIZE)

#To solve ILPP
model.optimize()

#Checking the Optime value
if model.status == GRB.OPTIMAL:
    print(f'Optimal objective Value: {model.ObjVal}')
    for i,j in G.edges():
        if (x[e(i,j)].X > 0.1):
            if (G.nodes[i]['label'] == 'people'):
                a = i
            if (G.nodes[i]['label'] == 'tasks'):
                b = i - n
            if (G.nodes[j]['label'] == 'people'):
                a = j 
            if (G.nodes[j]['label'] == 'tasks'):
                b = j - n
            print(f'Person {a} will make task {b} (x{i}{j} = {x[e(i,j)].X})')

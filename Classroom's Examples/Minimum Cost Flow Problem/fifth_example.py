import gurobipy as gb
from gurobipy import GRB
import networkx as nx

"""About the code address the problem the way of min cost.
   The goal this code be didatic and one form to learning """


#Create DiGraph
DG = nx.DiGraph()

#Creaty a array with nodes and edges
nodes = [(0,{'e':1 , 's':0}),
         (1,{'e':0 , 's':0}),
         (2,{'e':0 , 's':0}),
         (3,{'e':0 , 's':1}),
         (4,{'e':0 , 's':0})]

#Add nodes
DG.add_nodes_from(nodes)

#Add edges
DG.add_edges_from([(i,j,{"f":1,"c":-abs(j-i)}) for i in list(DG.nodes()) for j in list(DG.nodes()) if i != j])

#Output of check 
print(DG.nodes(data=True))
print(DG.edges(data=True))

#Creating the model
model = gb.Model('Problem')

x = {} #Create empty dictionary

#Creating variables
for i,j,d in DG.edges(data=True):
    x[(i,j)] = model.addVar(vtype=GRB.CONTINUOUS,name=f"x{i}{j}") 

#Creating restrictions 
for i,d in DG.nodes(data=True):
    #All that enter - out = s(out) - e(enter)
    model.addConstr( gb.quicksum(x[(i,j)] for i,j in DG.in_edges(i)) -gb.quicksum(x[(i,j)] for i,j in DG.out_edges(i)) == d["s"] - d["e"] )

for i,j,d in DG.edges(data=True):
    if i < j:
       #All come and back <= F
       model.addConstr(x[(i,j)] + x[(j,i)] <= d['f'])

#Creating Objective Function
model.setObjective(gb.quicksum(d['c']*x[(i,j)] for i,j,d in DG.edges(data=True)),GRB.MINIMIZE)

#Debug
model.write('model.lp')   

#To solve ILPP
model.optimize()

#Checking the Optime value
if model.status == GRB.OPTIMAL:
    print(f'Optimal objective Value: {model.ObjVal}')
    for i,j in DG.edges():
        if (x[(i,j)].X > 0.1):
            print(f'(x{i}{j} = {x[(i,j)].X})')
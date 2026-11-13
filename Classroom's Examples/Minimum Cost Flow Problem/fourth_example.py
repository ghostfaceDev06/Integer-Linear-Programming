import gurobipy as gb
from gurobipy import GRB

#Creating model
model = gb.Model('Coverage Problem')

cobert = {} #Create empty dictionary

#add elements 
cobert[0] = [0,3]
cobert[1] = [1,4]
cobert[2] = [2,5]
cobert[3] = [0,3,6]
cobert[4] = [1,4,7]
cobert[5] = [2,5,8]
cobert[6] = [3,6]
cobert[7] = [4,7]
cobert[8] = [5,8]

n = len(cobert) #Dimension of Coverage

x = {} #Create empty dictionary

#Creating variables
for i in range(n):
    x[i] = model.addVar(vtype=GRB.BINARY,name=f"x{i}")

#Creating restrictions
for a in cobert.values():
    model.addConstr(gb.quicksum(x[j] for j in a) >= 1)

#Creating Objective Function
model.setObjective(gb.quicksum(x[i] for i in range(n)),GRB.MINIMIZE)

#To solve ILPP
model.optimize()

#Checking the Optime value
if model.status == GRB.OPTIMAL:
    print(f'Optimal objective Value: {model.ObjVal}')
    for i in range(n):
        print(f'x{i} = {x[i].X}')
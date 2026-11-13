import gurobipy as gb #Module of Linear Programming Problem
from gurobipy import GRB

#Create a New Model
model = gb.Model('Sixth Example')

#Add the variables
x1 = model.addVar(vtype=GRB.CONTINUOUS,name='x0',lb=2)
x2 = model.addVar(vtype=GRB.CONTINUOUS,name='x1',lb=0,ub=1)
x3 = model.addVar(vtype=GRB.CONTINUOUS,name='x1',lb=1)
x4 = model.addVar(vtype=GRB.CONTINUOUS,name='x2',lb=0)

#Defining Objective Function
model.setObjective(5*x1 + 6*x2 + 5*x3 + 6*x4, GRB.MAXIMIZE)

#Defining Restrictions
model.addConstr(x1 + x2 + x3 + x4 <= 8, 'r1' )
model.addConstr(4*x1 + 2*x2 + 2*x3 + 6*x4 <= 31, 'r2')
model.addConstr(x1 + 3*x2 + x3 + x4 <= 11, 'r3' )
model.addConstr(2*x1 + 2*x2 + 4*x3 + 2*x4 <= 21, 'r4' )

#Optimize the model 
model.optimize()

#Print values 
if model.status == GRB.OPTIMAL:
    print(f'Optimal objective Value: {model.ObjVal}')
    print(f'Solve: x0 = {x1.X} \t x1 = {x2.X} \t x2 = {x3.X} \t x3 = {x4.X} ')

#This code use branch-bound

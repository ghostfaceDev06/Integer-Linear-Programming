import gurobipy as gb #Module of Linear Programming Problem
from gurobipy import GRB
""" First class about Inter Linear Programming"""
c = [2,3,2,5] #costs 
a = [1,1,2,3] # item's capacity 
cap = 3 # bag's capacity

#Create a New Model
model = gb.Model('First')

#Add the variables
x1 = model.addVar(vtype=GRB.BINARY,name='x1')
x2 = model.addVar(vtype=GRB.BINARY,name='x2')
x3 = model.addVar(vtype=GRB.BINARY,name='x3')
x4 = model.addVar(vtype=GRB.BINARY,name='x4')

#Defining Objective Function
model.setObjective(2*x1 + 3*x2 + 2*x3 + 5*x4, GRB.MAXIMIZE)

#Defining Restrictions
model.addConstr(x1 + x2 + 2*x3 + 3*x4 <= 3, 'r1' )

#Optimize the model 
model.optimize()

#Print values 
if model.status == GRB.OPTIMAL:
    print(f'Optimal objective Value: {model.ObjVal}')
    print(f'Solve: x1 = {x1.X} \t x2 = {x2.X} \t x3 = {x3.X} \t x4 = {x4.X} ')

'''This examples I learn how to devlop with Gurobipy Pyhton Library to solve Intergers Linear Programming´s Problems, in special the bag´s problem '''

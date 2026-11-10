import gurobipy as gb
from gurobipy import GRB

#Data of Problem
cost = [[1,2,2,1],  #Matrix of costs
        [0,3,2,1],
        [2,1,0,2],
        [1,0,3,3]]
n = len(cost[0]) #Dimension of matrix

#Modeling of Problem
#x[i,j] = 1 if person i does task j, 0 otherwise (binary)
#Max sum_i sum_j  cost[i][j] * x[i,j]
#s.t sum_j x[i,j] = 1 for each person i (each person does one task)
#    sum_i x[i,j] = 1 for each task j   (each task has one person)

#Creating model
assignment_model = gb.Model("Assignment Problem") #Put name on the model
x = {} #Create an empty dictionary to keep variables

for i in range(n):
    for j in range(n):
        x[(i,j)] = assignment_model.addVar(vtype=GRB.BINARY,name=f'x{i}{j}') #Create an variables of problem

for i in range(n): #For eacher person i
    assignment_model.addConstr(gb.quicksum(x[(i,j)] for j in range(n)) == 1) #Person i does exactly one task (i fixed, j runs over all tasks)

for j in range(n): #For eacher task j
    assignment_model.addConstr(gb.quicksum(x[(i,j)] for i in range(n)) == 1) #Task j is done by exactly one person (j fixed, i runs over all people)

assignment_model.setObjective(gb.quicksum(cost[i][j]*x[(i,j)] for i in range(n) for j in range(n)),GRB.MAXIMIZE) #Create the Objetive Function

assignment_model.optimize() #To solve the Assignment Problem

#Output 
if assignment_model.status == GRB.OPTIMAL:
    print(f'The Optimal Objective Value is {assignment_model.ObjVal}')
    for i in range(n):
        for j in range(n):
            print(f'x{i}{j} = {x[(i,j)].X}')
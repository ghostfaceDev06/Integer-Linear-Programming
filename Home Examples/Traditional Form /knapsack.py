import gurobipy as gb
from gurobipy import GRB

#Informations about the Knapsack Problem:
n = 4 #The numbers of variables
weight = [1,1,2,3] #The weights of variables that occupy in the bag
value = [2,3,2,5] #The values of variables in Objective Function
capacity = 3 #The bag's capacity

#Modeling of Problem
# x[i] = 1, if item is put in the bag
# x[i] = 0, if item is not put in the bag
#Max Plus_i value[i] * x[i]
#s.a Plus_i weight[i] * x[i] <= Capacity

#Building the model
knapsack_model = gb.Model("Knapsack Problem") #This line put name of model
x = knapsack_model.addVars(n,vtype=GRB.BINARY) #This line is responsible to create variables of problem and you see is type of binary
knapsack_model.addConstr(gb.quicksum(weight[i]*x[i] for i in range(n)) <= capacity) #This line is responsible for creation the restrictions
knapsack_model.setObjective(gb.quicksum(value[i]*x[i] for i in range(n)),GRB.MAXIMIZE) #This line is responsible for creation the Objective Function
knapsack_model.optimize() #This line to solve the Knapsack Problem

#Output of results
if knapsack_model.status == GRB.OPTIMAL:
    chosen = [ i for i in range(n) if x[i].X > 0.5]
    print(f'The Optimal value is {knapsack_model.ObjVal} and chosen variables are x{chosen}')
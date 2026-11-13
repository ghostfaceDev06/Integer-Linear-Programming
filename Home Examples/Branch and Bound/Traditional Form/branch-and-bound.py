import gurobipy as gb 
from gurobipy import GRB

#Data about Branch and Bound
costs = [5,6,5,6] #Objective coefficients (Max)
b = [8,31,11,21] #Right-Hand sides (all <=)
A = [[1,1,1,1],
     [4,2,2,6],
     [1,3,1,1],
     [2,2,4,2]] #Constraint coefficients, one row for each restriction
n = len(A[0]) #Dimension of Matrix

#Modeling of Problem
# x[i] >= 0 and integer
# Max sum_i costs[i]*x[i]
# s.t. sum_i A[k][i]*x[i] <= b[k] for each row k

#Creating Model
branch_and_bound_model = gb.Model("Branch and Bound")
x = branch_and_bound_model.addVars(n,vtype=GRB.INTEGER,lb=0) #Integer variables: optimize() runs the branch and bound
for k in range(len(b)):
    branch_and_bound_model.addConstr(gb.quicksum(A[k][i]*x[i] for i in range(n)) <= b[k])
branch_and_bound_model.setObjective(gb.quicksum(costs[i]*x[i] for i in range(n)),GRB.MAXIMIZE)
branch_and_bound_model.optimize()

#Output
if branch_and_bound_model.status == GRB.OPTIMAL:
    print(f'The optimal value is {branch_and_bound_model.ObjVal}')
    for i in x:
        print(f'x{i} = {x[i].X}')

#With relaxation
relaxed = branch_and_bound_model.relax()
relaxed.optimize()
print(f'With Relaxation the Optimal value is {relaxed.ObjVal}')
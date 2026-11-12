import gurobipy as gb
from gurobipy import GRB

#Data
n = 5 #Nodes 0..4
e = [1,0,0,0,0] #e[i] = 1: one unit enters the netwoek at node 0 (source)
s = [0,0,0,1,0] #s[i] = 1: one unit leaves the network at node 3 (sink)
cost = {(i,j): abs(j-i) for i in range(n) for j in range(n) if i != j} #cost[i,j] = |j-i|, only for i != j
cap = 1 #Capacity shared by each pair of nodes 

#Modeling of Problem
# x[i,j] = flow on the arc i -> j (continuous, x >= 0)
# Min  sum_{i != j} cost[i][j] * x[i,j]
# s.t. for each node i:  sum_j x[j,i] - sum_j x[i,j] = s[i] - e[i]   (flow balance)
#      for each pair i<j: x[i,j] + x[j,i] <= cap                     (capacity of the pair)

#Creating the model
mcfp_model = gb.Model("Minimum Cost Flow Problem")
x = {}

for i in range(n):
    for j in range(n):
        if i != j : x[(i,j)] = mcfp_model.addVar(vtype=GRB.CONTINUOUS,name=f"x{i}{j}") #One flow variable for each arc i -> j (no self-loops)

#in - out = s - e: the source sends one unit more than it receives, the sink receives one unit more than it sends
for i in range(n):
    mcfp_model.addConstr((gb.quicksum(x[(j,i)] for j in range(n) if j != i)  #Flow that enters i
                          - gb.quicksum(x[(i,j)] for j in range(n) if j != i))  #minus flow that leaves i
                            == s[i] - e[i]) #-1 at the source, +1 at the sink, 0 in the others

for i in range(n):
    for j in range(i+1,n): #Each pair of nodes only once (i < j)
        mcfp_model.addConstr(x[(i,j)] + x[(j,i)] <= cap) #Going and coming back together cannot pass the capacity

mcfp_model.setObjective(gb.quicksum(cost[i,j]*x[i,j] for (i,j) in cost),GRB.MINIMIZE)  #Total cost = sum of cost * flow of each arc
mcfp_model.optimize() #To solve Minimum Cost Flow Problem

#Output 
if mcfp_model.status == GRB.OPTIMAL:  #Only reads the variables if Gurobi found the optimum
    print(f'The Optimal value is {mcfp_model.ObjVal}') #Total cost of the solution
    for (i,j) in x: #The keys of x are the arcs (i,j)
        if x[i,j].X > 1e-6: #Flows are continuous, so any value above zero counts (not 0.5)
            print(f'x{i}{j} = {x[i,j].X}') #Flow on the arc i -> j
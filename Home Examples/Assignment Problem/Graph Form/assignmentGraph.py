import gurobipy as gb
from gurobipy import GRB
import networkx as nx

#Data of Problem
cost = [[1,2,2,1],  #Matrix of costs
        [0,3,2,1],
        [2,1,0,2],
        [1,0,3,3]]
n = len(cost[0]) #Dimension of matrix

#Modeling of Problem 
#Bipartite graph: nodes 0..n-1 are people, nodes n..2n-1 are tasks (task j = node n+j)
#Edge (i,n+j) has the attribute cost = cost[i][j]
#x[edge] = 1 if the edge is chosen (binary)
#Max sum over edges of cost[edge] * x[edge]
#s.t for each node v: sum of x over the edges that touch v == 1

def e(a,b): return (min(a,b),max(a,b)) # same key for an edge in any order

#Creating Graph
G = nx.Graph() #Undirected graph: an edge between person and task has no direction
for i in range(n): #i = 0..n-1, one node for each person
    G.add_node(i,label='people') #The node number is the person's index; label marks which side of the bipartite graph it is

for j in range(n,2*n): #j = n..2n-1, one node for each task (with n = 4: nodes 4, 5, 6, 7)
    G.add_node(j,label='tasks') #The node number is n + task index, so it does not collide with the people nodes

for i in range(n): #For each person i
    for j in range(n,2*n):  #For each task node j, so every person is connected to every task
        G.add_edge(i,j,cost = cost[i][j-n])  #Edge (person i, task node j) stores its cost; j-n converts the node number back to the column of c

#Creating model
assignment_graph = gb.Model("Assignment Graph") #Put name on the model
x = {} #Create an empty dictionary to keep variables

#Creating variables
for a,b,d in G.edges(data=True): #One iteration for each edge (i, j); d is its attribute dictionary, here {'cost': ...}
    x[e(a,b)] = assignment_graph.addVar(vtype=GRB.BINARY,name=f'x{i}{j}') #x = 1 if this person-task edge is chosen, 0 otherwise; e(i,j) gives the same key in any order

#Creating restrictions
for v in G.nodes():  #For each node v, that is a person or a task
    assignment_graph.addConstr(gb.quicksum(x[e(v,u)] for v,u in G.edges(v)) == 1)  #G.edges(v) lists the edges that touch v, so exactly one of them is chosen: the person does one task, or the task has one person

assignment_graph.setObjective(gb.quicksum(d['cost']*x[e(a,b)] for a,b,d in G.edges(data=True)),GRB.MAXIMIZE) #Creating Objective Function
assignment_graph.optimize() #To solve Assignment Problem

#Output
if assignment_graph.status == GRB.OPTIMAL:
    print(f'Optimal objective Value: {assignment_graph.ObjVal}')
    for u, v in G.edges(): #Each edge (u, v) of the graph
        if x[e(u, v)].X > 0.5: #Only the edges chosen by the solution
            person = min(u, v) #People are nodes 0..n-1, so the smaller node is the person
            task = max(u, v) - n #Tasks are nodes n..2n-1, so the bigger node minus n is the task index
            print(f'Person {person} will make task {task}')
import gurobipy as gb
from gurobipy import GRB
import numpy as np


A = np.array([[7, -2, 1, 0, 0, 0], [0, 1, 0, 1, 0, 0], [2, -2, 0, 0, 1, 0], [0, 0, 1/7, 2/7, 0, -1]])


gomori_model = gb.Model()
gomori_model.params.Presolve = 0
gomori_model.params.Method = 0
x={}
x[1] = gomori_model.addVar(vtype=GRB.CONTINUOUS,name='x1')
x[2] = gomori_model.addVar(vtype=GRB.CONTINUOUS,name='x2')
x[3] = gomori_model.addVar(vtype=GRB.CONTINUOUS,name='x3')
x[4] = gomori_model.addVar(vtype=GRB.CONTINUOUS,name='x4')
x[5] = gomori_model.addVar(vtype=GRB.CONTINUOUS,name='x5')
x[6] = gomori_model.addVar(vtype=GRB.CONTINUOUS,name='x6')

gomori_model.setObjective(59/7 -(4/7)*x[3] -x[4]/7,GRB.MAXIMIZE)

gomori_model.addConstr(x[1] == 20/7 - x[3]/7 - (2/7)*x[4])
gomori_model.addConstr(x[2] == 3 - x[4])
gomori_model.addConstr(x[5] == 23/7 - (2/7)*x[3] - (10/7)*x[4])
gomori_model.addConstr(x[3]/7 + (2/7)*x[4] - x[6] == 6/7)
#gomori_model.addConstr(

gomori_model.optimize()
IB=[]
IN=list(range(len(x.keys())))
IFrac=[]

if gomori_model.status == GRB.OPTIMAL:
    print(f'The optimal value is {gomori_model.ObjVal}')
    print(f'Solve: x1:{x[1].X}\tx2:{x[2].X}\tx3:{x[3].X}\tx4:{x[4].X}\tx5:{x[5].X}\tx6:{x[6].X}')
    
    for i in range(1,7):
        if x[i].X>0.00001:
            IB.append(i)
            IN.remove(i-1)
            if np.abs((x[i].X-np.floor(x[i].X)))>0.00000001:
                IFrac.append(i-1)
    B=A[:,[i-1 for i in IB]]
    N=A[:,IN]
    invB=np.linalg.inv(B)
    InvBN=invB@N
    print(f'tamanho de IFrac: {len(IFrac)}')
    if len(IFrac)>0:
        print(f'Variável com valor fracionário selecionada: {IFrac[0]}')
        gomorycoef=[a-np.floor(a) for a in InvBN[IFrac[0],:]]
        gomoryconst=x[IFrac[0]+1].X-np.floor(x[IFrac[0]+1].X)
        for i in range(len(gomorycoef)):
            a=gomorycoef[i]
            if (a>-0.0000001 and a<0.0000001):
                gomorycoef[i]=0
        print(f'variáveis não básicas: {[i+1 for i in IN]}')
        print(f'coeficiente gomory: {gomorycoef}')
        print(f'constante lado direito gomory: {gomoryconst}')

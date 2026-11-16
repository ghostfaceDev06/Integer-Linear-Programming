import gurobipy as gb
import numpy as np
from gurobipy import GRB

#=============================================================================
#Final Version: This version is the final implementation and has all cultures.
#=============================================================================

#=============================================
#Data about Integer Linear Programming Problem
#=============================================

#==================================================
#Where s = day that planted, t = day of restriction 
#==================================================
s,t = np.arange(1,29), np.arange(1,29)
T = s[-1]

#===================================================================
#Where cultures = Is dictionary keeps the informations about cultures
#===================================================================

cultures = {'Blue Jazz':{
    'Cost': 30,
    'Grow': 7,
    'Regrowth':None,
    'Energy to Water': 2,
    'Energy to Till':2,
    'Sell':50
    },

    'Cauliflower':{
    'Cost': 80,
    'Grow': 12,
    'Regrowth':None,
    'Energy to Water': 2,
    'Energy to Till':2,
    'Sell':175
    },

    'Kale':{
    'Cost': 70,
    'Grow': 6,
    'Regrowth':None,
    'Energy to Water': 2,
    'Energy to Till':2,
    'Sell':110   
    },

    'Parsnip':{
    'Cost': 20,
    'Grow': 4,
    'Regrowth':None,
    'Energy to Water': 2,
    'Energy to Till':2,
    'Sell':35    
    },

    'Potato':{
    'Cost': 50,
    'Grow': 6,
    'Regrowth':None,
    'Energy to Water': 2,
    'Energy to Till':2,
    'Sell':80
    },

    'Tulip':{
    'Cost': 20,
    'Grow': 6,
    'Regrowth':None,
    'Energy to Water': 2,
    'Energy to Till':2,
    'Sell':30
    },

    'Unmilled Rice':{
    'Cost': 40,
    'Grow': 6,
    'Regrowth':None,
    'Energy to Water': 2,
    'Energy to Till':2,
    'Sell':30
    },

    'Strawberry':{
    'Cost': 100,
    'Grow': 8,
    'Regrowth':4,
    'Energy to Water': 2,
    'Energy to Till':2,
    'Sell':120
    },

    'Green Bean':{
    'Cost': 60,
    'Grow': 10,
    'Regrowth':3,
    'Energy to Water': 2,
    'Energy to Till':2,
    'Sell':40
    }
}

#==================================================================================
#Where J1 = Only the cultures without regrowth, J2 = Only the cultures with regrowth
#==================================================================================
J1 = [j for j in cultures if cultures[j]['Regrowth'] == None]
J2 = [j for j in cultures if cultures[j]['Regrowth'] != None]

#========================================
# J2's number of haverst to end of season 
#========================================
def harvest(j,s,T):
    growth = cultures[j]["Grow"]
    regrowth = cultures[j]["Regrowth"]

    if T < s + growth:
        return 0
    else:
        return 1 + (T-s-growth)//regrowth

def H(j,s): return harvest(j,s,T)

#==================
#Creating the model
#==================
STDV_final_model = gb.Model("Stardew Valley Final Model")

#=======================
# Creating the variables
#=======================
x = {} 
for j in cultures:
    for s_x in s:
        if s_x + cultures[j]['Grow'] > s[-1]:
            continue
        if j == 'Strawberry' and s_x < 13:
            continue
        
        x[j,s_x] = STDV_final_model.addVar(vtype=GRB.INTEGER,lb=0,name=f'x{j}{s_x}')

#===========================
#Creating Objective Function
#===========================
J1_revenue = gb.quicksum(cultures[j]['Sell'] * x[j,day] for (j,day) in x if j in J1)
J2_revenue = gb.quicksum(cultures[j]['Sell'] * H(j,day) * x[j,day] for (j,day) in x if j in J2)
expenses = gb.quicksum(cultures[j]['Cost'] * x[j,day] for (j,day) in x)
STDV_final_model.setObjective(J1_revenue + J2_revenue - expenses,GRB.MAXIMIZE)

#====================================
#Creating First Restriction : Capital
#==================================== 
for t_x in t:
    J1_revenue_t = gb.quicksum(cultures[j]['Sell'] * x[j,day] for (j,day) in x if j in J1 and day + cultures[j]['Grow'] <= t_x)
    J2_revenue_t =  gb.quicksum(cultures[j]['Sell'] * harvest(j,day,t_x) * x[j,day] for (j,day) in x if j in J2)
    expenses_t = gb.quicksum(cultures[j]['Cost'] * x[j,day] for (j,day) in x if day <= t_x)
    STDV_final_model.addConstr(500 + J1_revenue_t + J2_revenue_t - expenses_t >= 0,name=f'Capital_{t_x}')

#====================================
#Creating Second Restriction : Energy
#====================================
for t_x in t:
    preparation = gb.quicksum(cultures[j]['Energy to Till'] * x[j,day] for (j,day) in x if day == t_x)
    J1_water = gb.quicksum(cultures[j]['Energy to Water'] * x[j,day] for (j,day) in x if j in J1 and day <= t_x < day + cultures[j]['Grow'])
    J2_water = gb.quicksum(cultures[j]['Energy to Water'] * x[j,day] for (j,day) in x if j in J2 and day <= t_x)
    STDV_final_model.addConstr(preparation + J1_water + J2_water <= 100, name=f'Energy{t_x}')   

#==================================
#Creating Third Restriction : Space
#==================================
for t_x in t:
    J1_space = gb.quicksum(x[j,day] for (j,day) in x if j in J1 and day <= t_x < day + cultures[j]['Grow'])
    J2_space = gb.quicksum(x[j,day] for (j,day) in x if j in J2 and day <= t_x)
    STDV_final_model.addConstr(J1_space + J2_space <= 40,name=f'Space{t_x}')   

#======
#Output
#======
STDV_final_model.optimize()
if STDV_final_model.status == GRB.OPTIMAL:
    print(f'The Optimal value is {STDV_final_model.ObjVal}')
    for (j_x,s_x) in x:
        if round(x[j_x,s_x].X) > 0:
           print(f'x{j_x}{s_x} = {x[j_x,s_x].X}')
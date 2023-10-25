import gurobipy as gp
from gurobipy import GRB

f = gp.Model('Electro-Poly')

m1 = f.addVar(name="number-model-1-in-house")
m2 = f.addVar(name="number-model-2-in-house")
m3 = f.addVar(name="number-model-3-in-house")
b1 = f.addVar(name="number-model-1-by-from-competitor")
b2 = f.addVar(name="number-model-2-by-from-competitor")
b3 = f.addVar(name="number-model-3-by-from-competitor")

f.setObjective(50*m1 + 83*m2 + 130*m3 + 61*b1 + 97*b2 + 145*b3, GRB.MINIMIZE)

f.addConstr(2*m1 + 1.5*m2 + 3*m3 <= 10000, "resource-wiring")
f.addConstr(1*m1 + 2*m2 + 1*m3 <= 5000, "resources-harnessing")

f.addConstr(1*m1 + 1*b1 == 3000, "demand-model-1")
f.addConstr(1*m2 + 1*b2 == 2000, "demand-model-2")
f.addConstr(1*m3+ 1*b3 == 900, "demand-model-3")

f.write('01-electro-poly-generated.lp')

f.optimize()

for v in f.getVars():
    print(v.varName, v.x)
print("optimal-value {}".format(f.objVal))
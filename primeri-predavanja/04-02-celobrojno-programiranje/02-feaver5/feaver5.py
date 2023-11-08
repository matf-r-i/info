import math
import pandas as pd

import xarray as xr 
from linopy import Model

m = Model()

x_coord = pd.Index(range(5), name='x_coord')
y_coord = pd.Index(range(5), name='y_coord')

x = m.add_variables(binary=True,  coords=[x_coord,y_coord], name='x')

y = m.add_variables(integer=True, lower=0, upper=2, coords=[x_coord,y_coord], name='y')

print(x)

# Objective function
m.add_objective( (x).sum(), sense='min')

# Constraints for inside fields
for i in range(1,4):
    for j in range(1,4):
        m.add_constraints(x.loc[i,j] + x.loc[i,j-1] + x.loc[i,j+1] + x.loc[i-1,j] + x.loc[i+1,j] - 2 * y.loc[i,j] == 1)
# Constraints for top and bottom border-line fields
for i in range(1,4):
    m.add_constraints(x.loc[i,0] + x.loc[i,1] + x.loc[i-1,0] + x.loc[i+1,0] - 2 * y.loc[i,0] == 1)
    m.add_constraints(x.loc[i,4] + x.loc[i,3] + x.loc[i-1,4] + x.loc[i+1,4] - 2 * y.loc[i,4] == 1)
# Constraints for left and right border-line fields
for j in range(1,4):
    m.add_constraints(x.loc[0,j] + x.loc[1,j] + x.loc[0,j-1] + x.loc[0,j+1] - 2 * y.loc[0,j] == 1)
    m.add_constraints(x.loc[4,j] + x.loc[3,j] + x.loc[4,j-1] + x.loc[4,j+1] - 2 * y.loc[4,j] == 1)
# Constraints for four end fields
m.add_constraints(x.loc[0,0] + x.loc[0,1] + x.loc[1,0] - 2 * y.loc[0,0] == 1)
m.add_constraints(x.loc[0,4] + x.loc[0,3] + x.loc[1,4] - 2 * y.loc[0,4] == 1)
m.add_constraints(x.loc[4,0] + x.loc[3,0] + x.loc[4,1] - 2 * y.loc[4,0] == 1)
m.add_constraints(x.loc[4,4] + x.loc[3,4] + x.loc[4,3] - 2 * y.loc[4,4] == 1)

print(m)

m.solve()

print(m.solution)

print("{}:\n{}\n".format(x, x.solution))
print("{}:\n{}\n".format(y, y.solution))

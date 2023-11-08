import math
import xarray as xr 
from linopy import Model

m = Model()

lower = xr.DataArray([0,0,0], dims=['from'])
upper = xr.DataArray([math.inf, math.inf, math.inf], dims=['to'])

x = m.add_variables(lower=lower, upper=upper, name='x')

print(x)

# Supply constrains
m.add_constraints(x.loc[0,0]+x.loc[0,1]+x.loc[0,2] == 275000)
m.add_constraints(x.loc[1,0]+x.loc[1,1]+x.loc[1,2] == 400000)
m.add_constraints(x.loc[2,0]+x.loc[2,1]+x.loc[2,2] == 300000)

# Capacity constrains
m.add_constraints(x.loc[0,0]+x.loc[1,0]+x.loc[2,0] <= 200000)
m.add_constraints(x.loc[0,1]+x.loc[1,1]+x.loc[2,1] <= 600000)
m.add_constraints(x.loc[0,2]+x.loc[1,2]+x.loc[2,2] <= 225000)

m.add_objective(  21*x.loc[0,0] + 50*x.loc[0,1] + 40*x.loc[0,2] 
                + 35*x.loc[1,0] + 30*x.loc[1,1] + 22*x.loc[1,2]
                + 55*x.loc[2,0] + 20*x.loc[2,1] + 25*x.loc[2,2])

print(m)

m.solve()

print(m.solution)

print("{}:\n{}\n".format(x, x.solution))


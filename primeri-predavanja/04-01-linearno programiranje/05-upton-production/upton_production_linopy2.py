import xarray as xr
from linopy import Model

m = Model()

lower = xr.DataArray([0,0,0,0,0,0])
p = m.add_variables(lower=lower, name='p')

lower = xr.DataArray([0,0,0,0,0,0,0])
b = m.add_variables(lower=lower, name='b')

print(m.variables)
print(p)

# constraints on production levels
level_min = xr.DataArray([2000, 1750, 2000, 2250, 2000, 1750])
m.add_constraints(p >= level_min, name="month production lower bound")
level_max = 2 * level_min
m.add_constraints(p <= level_max, name="month production upper bound")

# constraints on ending inventory (EI = BI+P-D)
demands = xr.DataArray([1000, 4500, 6000, 5500, 3500, 4000])
m.add_constraints(b+p-demands >= 1500, name="ending inventory lower bound")
m.add_constraints(b+p-demands <= 6000, name="ending inventory upper bound")

# beginning balances
m.add_constraints(b.loc[0] == 2750, name="month 1 beginning balance")
m.add_constraints(b.loc[1] == b.loc[0]+p.loc[0]-demands[0], name="month 2 beginning balance")
m.add_constraints(b.loc[2] == b.loc[1]+p.loc[1]-demands[1], name="month 3 beginning balance")
m.add_constraints(b.loc[3] == b.loc[2]+p.loc[2]-demands[2], name="month 4 beginning balance")
m.add_constraints(b.loc[4] == b.loc[3]+p.loc[3]-demands[3], name="month 5 beginning balance")
m.add_constraints(b.loc[5] == b.loc[4]+p.loc[4]-demands[4], name="month 6 beginning balance")
m.add_constraints(b.loc[6] == b.loc[5]+p.loc[5]-demands[5], name="month 7 beginning balance")

costs_production = xr.DataArray([240, 250, 265, 285, 280, 260])
costs_inventory = xr.DataArray( 
    [3.6, 3.6/2+3.75/2, 3.75/2+3.98/2, 3.98/2+4.28/2, 4.28/2+4.20/2, 4.20/2+3.9/2, 3.9/2])
m.add_objective((p*costs_production).sum()+(b*costs_inventory).sum())

print(m)

m.solve()

print(m.solution)

print(p)
print(p.solution)

print(b)
print(b.solution)

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
m.add_constraints(p.loc[0] >= 2000, name="month 1 lower bound - production")
m.add_constraints(p.loc[0] <= 4000, name="month 1 upper bound - production")
m.add_constraints(p.loc[1] >= 1750, name="month 2 lower bound - production")
m.add_constraints(p.loc[1] <= 3500, name="month 2 upper bound - production")
m.add_constraints(p.loc[2] >= 2000, name="month 3 lower bound - production")
m.add_constraints(p.loc[2] <= 4000, name="month 3 upper bound - production")
m.add_constraints(p.loc[3] >= 2250, name="month 4 lower bound - production")
m.add_constraints(p.loc[3] <= 4500, name="month 4 upper bound - production")
m.add_constraints(p.loc[4] >= 2000, name="month 5 lower bound - production")
m.add_constraints(p.loc[4] <= 4000, name="month 5 upper bound - production")
m.add_constraints(p.loc[5] >= 1750, name="month 6 lower bound - production")
m.add_constraints(p.loc[5] <= 3500, name="month 6 upper bound - production")

# constraints on ending inventory (EI = BI+P-D)
m.add_constraints(b.loc[0]+p.loc[0]-1000 >= 1500, name="month 1 lower bound - ending inventory")
m.add_constraints(b.loc[0]+p.loc[0]-1000 <= 6000, name="month 1 upper bound - ending inventory")
m.add_constraints(b.loc[1]+p.loc[1]-4500 >= 1500, name="month 2 lower bound - ending inventory")
m.add_constraints(b.loc[1]+p.loc[1]-4500 <= 6000, name="month 2 upper bound - ending inventory")
m.add_constraints(b.loc[2]+p.loc[2]-6000 >= 1500, name="month 3 lower bound - ending inventory")
m.add_constraints(b.loc[2]+p.loc[2]-6000 <= 6000, name="month 3 upper bound - ending inventory")
m.add_constraints(b.loc[3]+p.loc[3]-5500 >= 1500, name="month 4 lower bound - ending inventory")
m.add_constraints(b.loc[3]+p.loc[3]-5500 <= 6000, name="month 4 upper bound - ending inventory")
m.add_constraints(b.loc[4]+p.loc[4]-3500 >= 1500, name="month 5 lower bound - ending inventory")
m.add_constraints(b.loc[4]+p.loc[4]-3500 <= 6000, name="month 5 upper bound - ending inventory")
m.add_constraints(b.loc[5]+p.loc[5]-4000 >= 1500, name="month 6 lower bound - ending inventory")
m.add_constraints(b.loc[5]+p.loc[5]-4000 <= 6000, name="month 6 upper bound - ending inventory")

# beginning balances
m.add_constraints(b.loc[0] == 2750, name="month 1 beginning balance")
m.add_constraints(b.loc[1] == b.loc[0]+p.loc[0]-1000, name="month 2 beginning balance")
m.add_constraints(b.loc[2] == b.loc[1]+p.loc[1]-4500, name="month 3 beginning balance")
m.add_constraints(b.loc[3] == b.loc[2]+p.loc[2]-6000, name="month 4 beginning balance")
m.add_constraints(b.loc[4] == b.loc[3]+p.loc[3]-5500, name="month 5 beginning balance")
m.add_constraints(b.loc[5] == b.loc[4]+p.loc[4]-3500, name="month 6 beginning balance")
m.add_constraints(b.loc[6] == b.loc[5]+p.loc[5]-4000, name="month 7 beginning balance")

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

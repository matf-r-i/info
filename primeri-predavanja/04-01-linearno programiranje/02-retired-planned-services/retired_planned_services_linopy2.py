import xarray as xr
from linopy import Model

m = Model()

lower = xr.DataArray([0,0,0,0,0,0])

x = m.add_variables(lower=lower, upper=187500, name='x')

print(m.variables)
print(x)

m.add_constraints((x).sum() == 750000, name="Total amount invested")

long_term = xr.DataArray([1,1,0,1,0,1])
m.add_constraints( (x*long_term).sum() >= 375000, name="Long term investment 50 percent restriction")

restriction_ds_ev_op = xr.DataArray([0,1,1,0,1,0])
m.add_constraints( (x*restriction_ds_ev_op).sum() <= 262500, name="Restriction on DynaStar, Eagle Vision and OptiPro")

gain = xr.DataArray([0.0865, 0.95, 0.1, 0.0875, 0.0925, 0.09])
m.add_objective((x*gain).sum())

print(m)

m.solve()

print(m.solution)


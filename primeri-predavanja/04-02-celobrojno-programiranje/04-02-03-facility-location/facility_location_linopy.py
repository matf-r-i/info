# Facility location problem can be described terms as follows:
# We must decide the placement of a group of facilities that distribute a certain good to a group of consumers that need it.
# The placement must to be chosen in order to minimize the distribution costs and fulfilling a set of possible additional constraints like building budget or maximum number of facilities.
# In a first stage, let’s make the following assumptions:
# 1. The possible locations for the facilities are known.
# 2. The facility building costs are fixed and known. This cost is paid only if we decide that the facility is going to be installed.
# 3. The transportation costs are known. For example we can imagine that the transport cost is proportional to the total distance covered in the good distribution.
# 4. Each facility can, if necessary, provide the all the demand.
# Notice that in this scenario there are two possible decision to be maid:
# (1) which facilities will be built and
# (2) which facility will serve each consumer.
# The objective of this assignment is to find an optimal placement of the facilities by formulating the problem as a Mixed Linear Integer Programming problem.

import math

import pandas as pd
from plotnine import ggplot, aes, geom_line, geom_point

import xarray as xr 
from linopy import Model

# Load data
consumer_locations = pd.read_csv('04-02-celobrojno-programiranje/04-02-03-facility-location/data/consumer_locations_01.csv', usecols= ['x','y'])
#print(consumer_locations)
facility_locations = pd.read_csv('04-02-celobrojno-programiranje/04-02-03-facility-location/data/facility_locations_01.csv', usecols= ['x','y'])
#print(facility_locations)
building_costs = pd.read_csv('04-02-celobrojno-programiranje/04-02-03-facility-location/data/building_costs_01.csv', usecols= ['building_costs'])
#print(building_costs)

# Create helper function for distance calculation between consumer and facility
def distance(i:int, j:int)->float:
    consumer = consumer_locations.loc[i]
    facility = facility_locations.loc[j]
    return math.sqrt( (consumer.x-facility.x) * (consumer.x-facility.x) 
            + (consumer.y-facility.y) * (consumer.y-facility.y))

print(distance(1,2))

# Draw loaded data on screen
draw = (
    ggplot(consumer_locations)  
    + aes(x="x", y="y")  
    + geom_point() 
    + geom_point(data = facility_locations, color = "red", alpha = 0.5) 
)
#print(draw)

# Obtain model dimension
n:int = consumer_locations.shape[0]
m:int = facility_locations.shape[0] 

# Create distance matrix
dists = []
for i in range(n):
    row = []
    for j in range(m):
        row.append(distance(i,j))
    dists.append(row)
distances = xr.DataArray(dists) 
#print(distances)

# Create building costs matrix
build_cs = []
for j in range(m):
    build_cs.append(building_costs.loc[j].building_costs)
build_costs = xr.DataArray(build_cs) 
#print(build_costs)

# Create an ILP model
model = Model()

x_coord = pd.Index(range(n), name='x_coord')
y_coord = pd.Index(range(m), name='y_coord')

x = model.add_variables(binary=True,  coords=[x_coord,y_coord], name='x')

y = model.add_variables(binary=True, coords=[y_coord], name='y')

#print(x)
#print(y)

# Objective function
model.add_objective( (x*distances).sum() + (build_costs*y).sum(), sense='min')

# Constraint: each consumer is served by one facility
for i in range(n):
    model.add_constraints( (x.loc[i,]).sum() == 1)

# Constraint: each consumer can be supplied from one established facility 
for i in range(n):
    for j in range(m):
        model.add_constraints(x.loc[i,j] <= y.loc[j])

# Constraint: there have to be exactly 2 established facilities 
model.add_constraints( (y).sum() == 2)

print(model)

model.solve()

print(model.solution)

print("{}:\n{}\n".format(x, x.solution))
print("{}:\n{}\n".format(y, y.solution))

selected = []
for i in range(len(y.solution.data)):
    if y.solution.data[i] > 0:
        selected.append([facility_locations.loc[i].x, facility_locations.loc[i].y])
print(selected)
selected = pd.DataFrame(selected, columns=['x', 'y'])

links = []





from linopy import Model

m = Model()

x1 = m.add_variables(lower=0, name='x1')
x2 = m.add_variables(lower=0, name='x2')
x3 = m.add_variables(lower=0, name='x3')
x4 = m.add_variables(lower=0, name='x4')

# Overall production
m.add_constraints(x1 + x2 + x3 + x4 == 8)

# mix consists of at least 20% corn  
m.add_constraints((0.3*x1 + 0.05*x2 + 0.2*x3 + 0.1*x4)/8 >= 0.2)

# mix consists of at least 15% grain  
m.add_constraints((0.1*x1 + 0.3*x2 + 0.15*x3 + 0.1*x4)/8 >= 0.15)

# mix consists of at least 15% minerals  
m.add_constraints((0.2*x1 + 0.2*x2 + 0.2*x3 + 0.3*x4)/8 >= 0.15)

m.add_objective( 250*x1 + 300*x2 + 320*x3 + 150*x4)

print(m)

m.solve()

print(m.solution)

print("{}:{}\n".format(x1, x1.solution))
print("{}:{}\n".format(x2, x2.solution))
print("{}:{}\n".format(x3, x3.solution))
print("{}:{}\n".format(x4, x4.solution))


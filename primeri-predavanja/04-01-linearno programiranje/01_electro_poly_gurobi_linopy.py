from linopy import Model

m = Model()

m1 = m.add_variables(lower=0, name="Number of model 1 to be build in house")
m2 = m.add_variables(lower=0, name="Number of model 2 to be build in house")
m3 = m.add_variables(lower=0, name="Number of model 3 to be build in house")
b1 = m.add_variables(lower=0, name="Number of model 1 to be bought from competitor")
b2 = m.add_variables(lower=0, name="Number of model 2 to be bought from competitor")
b3 = m.add_variables(lower=0, name="Number of model 3 to be bought from competitor")

m.add_constraints(2*m1 + 1.5*m2 + 3*m3 <= 10000, name="Resources wiring constraint")
m.add_constraints(m1 + 2*m2 + m3 <= 5000, name="Resources harnessing constraint")

m.add_constraints(m1 + b1 == 3000, name="Demand for model 1")
m.add_constraints(m2 + b2 == 2000, name="Demand for model 2")
m.add_constraints(m3+ b3 == 900, name="Demand for model 3")

m.add_objective(50*m1 + 83*m2 + 130*m3 + 61*b1 + 97*b2 + 145*b3)

print(m)

m.solve()

print("{}:{}\n".format(m1, m1.solution))
print("{}:{}\n".format(m2, m2.solution))
print("{}:{}\n".format(m3, m3.solution))
print("{}:{}\n".format(b1, b1.solution))
print("{}:{}\n".format(b2, b2.solution))
print("{}:{}\n".format(b3, b3.solution))


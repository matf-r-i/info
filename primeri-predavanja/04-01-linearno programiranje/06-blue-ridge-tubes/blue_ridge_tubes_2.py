from linopy import Model

m = Model()

x1 = m.add_variables(lower=0, name="x1")
x2 = m.add_variables(lower=0, name="x2")

m.add_constraints(x1 + x2 <= 200, name="pumps constraint")
m.add_constraints(9*x1 + 6*x2 <= 1520, name="labor constraint")
m.add_constraints(12*x1 + 16*x2 <= 2650, name="tubing constraint")

m.add_objective(-(350*x1 + 300*x2))

print(m)

m.solve()

print("{}:{}\n".format(x1, x1.solution))
print("{}:{}\n".format(x2, x2.solution))


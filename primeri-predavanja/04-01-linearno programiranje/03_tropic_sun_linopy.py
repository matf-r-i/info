from linopy import Model

m = Model()

x14 = m.add_variables(lower=0)
x15 = m.add_variables(lower=0)
x16 = m.add_variables(lower=0)
x24 = m.add_variables(lower=0)
x25 = m.add_variables(lower=0)
x26 = m.add_variables(lower=0)
x34 = m.add_variables(lower=0)
x35 = m.add_variables(lower=0)
x36 = m.add_variables(lower=0)

# Supply constrains
m.add_constraints(x14 + x15 + x16 == 275000)
m.add_constraints(x24 + x25 + x26 == 400000)
m.add_constraints(x34 + x35 + x36 == 300000)

# Capacity constrains
m.add_constraints(x14 + x24 + x34 <= 200000)
m.add_constraints(x15 + x25 + x35 <= 600000)
m.add_constraints(x16 + x26 + x36 <= 225000)

m.add_objective( 21*x14 + 50*x15 + 40*x16 
        + 35*x24 + 30*x25 + 22*x26
        + 55*x34 + 20*x35 + 25*x36)

print(m)

m.solve()

print(m.solution)

print("{}:{}\n".format(x14, x14.solution))
print("{}:{}\n".format(x15, x15.solution))
print("{}:{}\n".format(x16, x16.solution))
print("{}:{}\n".format(x24, x24.solution))
print("{}:{}\n".format(x25, x25.solution))
print("{}:{}\n".format(x26, x26.solution))
print("{}:{}\n".format(x34, x34.solution))
print("{}:{}\n".format(x35, x35.solution))
print("{}:{}\n".format(x36, x36.solution))


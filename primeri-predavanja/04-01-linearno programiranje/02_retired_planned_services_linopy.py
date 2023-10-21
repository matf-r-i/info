from linopy import Model

m = Model()

x1 = m.add_variables(lower=0, name="Money to invest in Acme Chemical")
x2 = m.add_variables(lower=0, name="Money to invest in DynaStar")
x3 = m.add_variables(lower=0, name="Money to invest in Eagle Vision")
x4 = m.add_variables(lower=0, name="Money to invest in MicroModeling")
x5 = m.add_variables(lower=0, name="Money to invest in OptiPro")
x6 = m.add_variables(lower=0, name="Money to invest in Sabre Systems")

m.add_constraints(x1 + x2 + x3 + x4 + x5 + x6 == 750000, name="Total amount invested")

m.add_constraints(x1 <= 187500, name="No more than 25 percent investment on Acme Chemical")
m.add_constraints(x2 <= 187500, name="No more than 25 percent investment on DynaStar")
m.add_constraints(x3 <= 187500, name="No more than 25 percent investment on Eagle Vision")
m.add_constraints(x4 <= 187500, name="No more than 25 percent investment on MicroModeling")
m.add_constraints(x5 <= 187500, name="No more than 25 percent investment on OptiPro")
m.add_constraints(x6 <= 187500, name="No more than 25 percent investment on Sabre Systems")

m.add_constraints(x1 + x2 + x4 + x6 >= 375000, name="Long term investment 50 percent restriction")

m.add_constraints(x2 + x3 + x5 <= 262500, name="Restriction on DynaStar, Eagle Vision and OptiPro")

m.add_objective(0.0865*x1 + 0.95*x2 + 0.1*x3 + 0.0875*x4 + 0.0925*x5 + 0.09*x6)

print(m)

m.solve()

print("{}:{}\n".format(x1, x1.solution))
print("{}:{}\n".format(x2, x2.solution))
print("{}:{}\n".format(x3, x3.solution))
print("{}:{}\n".format(x4, x4.solution))
print("{}:{}\n".format(x5, x5.solution))
print("{}:{}\n".format(x6, x6.solution))


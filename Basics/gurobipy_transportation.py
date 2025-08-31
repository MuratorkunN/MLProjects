import gurobipy as gp

# Solving the transportation problem using gurobipy

m = gp.Model("TransportationProblem")

source_set, destination_set = range(3), range(4)

cost_table = {(0,0):10, (0,1):0, (0,2):20, (0,3):11,
(1,0):12, (1,1):7, (1,2):9, (1,3):20,
(2,0):0, (2,1):14, (2,2):16, (2,3):18}
supplies = {0:1400, 1:2300, 2:800}
demands = {0:500, 1:1500, 2:1500, 3:1000}

x = m.addVars(source_set, destination_set, vtype= gp.GRB.CONTINUOUS, name = "amount", lb = 0)

#print(type(x)) -> tuple dictionary

obj_expr = gp.quicksum(cost_table[i, j] * x [i, j]
                       for i in source_set for j in destination_set)

# Better way of doing the same:
# obj_expr = gp.quicksum(cost_table[i, j] * x[i, j] for (i, j) in x.keys())

m.setObjective(obj_expr, sense = gp.GRB.MINIMIZE)

for i in source_set:
    lhs = gp.quicksum(x[i, j] for j in destination_set)
    m.addConstr(lhs <= supplies[i])

for j in destination_set:
    lhs = gp.quicksum(x[i, j] for i in source_set)
    m.addConstr(lhs >= demands[j])

m.optimize()
m.printAttr("objval")
m.printAttr("x")
import gurobipy as gp

# Finding the optimal solution for knapsack 0-1 problem using gurobipy.

m = gp.Model("Knapsack_01")

item_set = range(6)

capacity = 20
values = {0:9, 1:175, 2:200, 3:28, 4:20, 5:50}
weights = {0:1, 1:10, 2:20, 3:7, 4:4, 5:2}

x = m.addVars(item_set, vtype=gp.GRB.BINARY, name = "item")

obj_expr = gp.quicksum(values[item] * x[item] for item in item_set)

m.setObjective(obj_expr, sense = gp.GRB.MAXIMIZE)

m.addConstr(gp.quicksum(weights[item] * x[item] for item in item_set) <= capacity)

m.optimize()
m.printAttr("objval")
m.printAttr("x")

# As seen in the result, the optimal solution is different from the solution found using greedy.

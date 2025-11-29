customer_demands = [4, 5, 6, 3]
facility_capacities = [10, 12]
facility_costs = [20, 18]

transportation_cost = [[3, 4],
                       [2, 5],
                       [6, 3],
                       [4, 2]]

l = [4, 3, 5, 2]

def knapsack_facility(demand, capacity, cost, transportation, lagrange):
    profit = []
    for i in range(len(demand)):
        for j in range(len(capacity)):
            profit.append(lagrange[i] - transportation[i][j] * demand[i])
        print(profit)


knapsack_facility(customer_demands, facility_capacities, facility_costs, transportation_cost, l)
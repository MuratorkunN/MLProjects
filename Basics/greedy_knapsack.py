import math

# Solving knapsack 0-1 problem using greedy.
# Note that greedy heuristic algorithm doesn't always lead to the optimal solution.

def knapsack_greedy(capacity, item_list, value_list, weight_list):
    if capacity <= 0:
        obj_value, solution = -math.inf, []

    else:
        obj_value, solution, slack = 0, [], capacity
        v2w_ratio = {item: value_list[item] / weight_list[item] for item in item_list}
        order = sorted(item_list, key=lambda item: v2w_ratio[item], reverse=True)

        for item in order:
            if weight_list[item] < slack:
                solution.append(item)
                slack -= weight_list[item]
                obj_value += value_list[item]

    return obj_value, solution

my_items = ("book", "clock", "computer", "painting", "radio", "vase")
my_capacity = 20
my_vals = dict(zip(my_items, (9, 175, 200, 99, 20, 50)))
my_weights = dict(zip(my_items, (1, 10, 20, 9, 4, 2)))

my_result = knapsack_greedy(my_capacity, my_items, my_vals, my_weights)
print(my_result)
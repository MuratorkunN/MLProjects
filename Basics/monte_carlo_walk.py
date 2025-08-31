import numpy as np
from monte_carlo import MonteCarloModel, MonteCarloSimulation

rng = np.random.default_rng()

# A drunk man steps to the left or right, by 50% chance each.
# Finding the expected number of steps before hitting a wall which is 10 steps away (-10, +10).

class DrunkWalk(MonteCarloModel):
    def __init__(self, wall_distance):
        self.wall_distance = wall_distance
        self.num_steps = 0
        self.position = 0
        self.game = []

    def run(self):
        while -10 < self.position < 10:
            step = rng.integers(0, 2)
            if step == 0:
                self.position -= 1
                self.num_steps += 1
                self.game.append(self.position)
            else:
                self.position += 1
                self.num_steps += 1
                self.game.append(self.position)

        # print(self.game)
        return self.num_steps

    def reset(self):
        self.num_steps = 0
        self.position = 0
        self.game = []

model = DrunkWalk(10)
# model.run()

sim = MonteCarloSimulation(10000, model) # the result is pretty close to 10^2
sim.replicate()
sim.display_hist()
print(sim.get_mean())

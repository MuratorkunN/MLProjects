import numpy as np
from monte_carlo import MonteCarloModel, MonteCarloSimulation

rng = np.random.default_rng()

# The game will continue as you roll a bigger number than your last roll. Include the last roll.
# Expected value of the game length.

class DiceGame(MonteCarloModel):
    def __init__(self):
        self.rolls = []
        self.score = 0

    def run(self):
        first_roll = rng.integers(1, 7, 1)
        self.rolls.append(first_roll)
        self.score += 1

        while True:
            roll = rng.integers(1, 7, 1)
            self.rolls.append(roll)
            self.score += 1
            if roll < self.rolls[-2]:
                break

        # print(self.rolls)
        return self.score

    def reset(self):
        self.rolls = []
        self.score = 0

model = DiceGame()
# model.run()

# Repeating the model many times so that we get a result much closer to the actual result.

sim = MonteCarloSimulation(100000, model)
sim.replicate()
sim.display_hist()
print(sim.get_mean())
"""

a class needed for running monte carlo models and simulations.
most of it taken from @author: ismailb

"""

import numpy as np
from matplotlib import pyplot as plt


class MonteCarloModel():
    def __init__(self):
        print("you need to override __init__ method.")

    def run(self):
        print("you need to override run method.")

    def reset(self):
        print("you need to override reset method.")


class MonteCarloSimulation():

    def __init__(self, number, MonteCarloModel):
        self.n, self.model = number, MonteCarloModel
        self.outputs = np.empty(number)  # An empty array that will hold replication outputs.
        self.avg = None

    def replicate(self):
        for i in range(self.n):
            self.outputs[i] = self.model.run()
            self.model.reset()
        self.avg = np.mean(self.outputs)

    def get_mean(self):
        if self.avg:
            return self.avg
        else:
            print("replicate your model first.")

    def display_hist(self, bins=20):

        if self.avg:
            if self.n >= 30:
                plt.figure()
                plt.title("Histogram of Replication Outputs")
                plt.xlabel("Observations")
                plt.ylabel("Frequencies")
                plt.hist(self.outputs, bins=bins, color="purple", edgecolor="black")
                plt.axvline(self.avg, linestyle="dotted", linewidth=3, color="black",
                            label=f"Mean Estimate: {round(self.avg, 2)}")
                plt.legend()
                plt.show()
            else:
                t = "at least 30 replications for a sensible histogram."
                print(t)
        else:
            print("replicate your model first.")


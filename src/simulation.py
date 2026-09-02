import numpy as np

from src.metrics import (
    average_pairwise_distance,
    distance_to_target,
    target_reached,
)

class Simulation:
   
    #Controls the execution of a SwarmSense simulation.

    def __init__(self, swarm, steps=100):
        self.swarm = swarm
        self.steps = steps
        self.results = []

    def run(self):
        #Run the simulation and record metrics at each step

        for step in range(self.steps):
            self.swarm.step()

            result = {
                "step": step,
                "average_pairwise_distance": average_pairwise_distance(self.swarm),
                "distance_to_target": distance_to_target(self.swarm),
                "target_reached": target_reached(self.swarm),
                "collisions": self.swarm.count_collisions(),
            }

            self.results.append(result)
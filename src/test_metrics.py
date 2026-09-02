import sys

sys.path.append("src")

import numpy as np

from config import SimulationConfig
from swarm import Swarm

from metrics import (
    average_pairwise_distance,
    distance_to_target,
    target_reached,
)


np.random.seed(42)


config = SimulationConfig(
    num_robots=5,
    world_size=10,
)


swarm = Swarm(
    config=config,
    target_position=[8.0, 8.0],
)


print(
    "Average pairwise distance:",
    average_pairwise_distance(swarm)
)

print(
    "Distance to target:",
    distance_to_target(swarm)
)

print(
    "Target reached:",
    target_reached(swarm)
)
print("\nSimulation:")

for step in range(20):

    swarm.step()

    print(
        f"Step {step + 1:02d} | "
        f"Swarm spread: "
        f"{average_pairwise_distance(swarm):.2f} | "
        f"Target distance: "
        f"{distance_to_target(swarm):.2f} | "
        f"Reached: "
        f"{target_reached(swarm)}"
    )
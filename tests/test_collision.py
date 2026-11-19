import sys

sys.path.append("src")

import numpy as np

from src.robot import Robot
from src.swarm import Swarm


swarm = Swarm(
    num_robots=2,
    world_size=10,
)


swarm.robots[0].position = np.array(
    [5.0, 5.0]
)

swarm.robots[1].position = np.array(
    [5.1, 5.0]
)


print(
    "Collisions:",
    swarm.count_collisions()
)
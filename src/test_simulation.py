import sys

sys.path.append("src")

import numpy as np

from swarm import Swarm
from simulation import Simulation


np.random.seed(42)


swarm = Swarm(
    num_robots=20,
    world_size=10,
    sensing_radius=2.0,
    target_position=[8.0, 8.0],
)


simulation = Simulation(
    swarm=swarm,
    steps=100,
)


print("Initial positions:")

for robot in swarm.robots[:3]:
    print(robot.id, robot.position)


simulation.run()


print("\nPositions after simulation:")

for robot in swarm.robots[:3]:
    print(robot.id, robot.position)
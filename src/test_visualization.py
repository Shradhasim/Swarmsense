import sys

sys.path.append("src")

import numpy as np

from swarm import Swarm
from visualization import SwarmVisualizer


np.random.seed(42)


swarm = Swarm(
    num_robots=20,
    world_size=10,
    sensing_radius=2.0,
    target_position=[8.0, 8.0],
)


visualizer = SwarmVisualizer(swarm)


for step in range(200):

    swarm.step()

    visualizer.draw()
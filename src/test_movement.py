import sys

sys.path.append("src")

import numpy as np

from swarm import Swarm


np.random.seed(42)


swarm = Swarm(
    num_robots=20,
    world_size=10,
    sensing_radius=2.0,
    target_position=[8.0, 8.0],
)

print("Target:", swarm.target_position)


def average_velocity():

    velocities = np.array(
        [robot.velocity for robot in swarm.robots]
    )

    return np.mean(velocities, axis=0)


print("Initial average velocity:")
print(average_velocity())


for step in range(10):

    swarm.step()

    print(
        f"Step {step + 1}:",
        average_velocity()
    )
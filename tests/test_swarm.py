import sys

sys.path.append("src")

from swarm import Swarm
from config import SimulationConfig

config = SimulationConfig(
    num_robots=20,
    world_size=10,
    sensing_radius=2.0,
)

swarm = Swarm(
    config=config,
    target_position=[8.0, 8.0],
)


print("Number of robots:", len(swarm.robots))


robot = swarm.robots[0]

print(
    "Robot 0 position:",
    robot.position
)

print(
    "Robot 0 velocity:",
    robot.velocity
)


neighbors = swarm.get_neighbors(robot)

print(
    "Robot 0 has",
    len(neighbors),
    "neighbors"
)

print(
    "Neighbor IDs:",
    [neighbor.id for neighbor in neighbors]
)
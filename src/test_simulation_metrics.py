import numpy as np

from config import SimulationConfig
from swarm import Swarm
from simulation import Simulation


np.random.seed(42)

config = SimulationConfig(
    num_robots=5
)

swarm = Swarm(config=config)

simulation = Simulation(
    swarm=swarm,
    steps=10
)

simulation.run()

print("Simulation results:")

for result in simulation.results:
    print(result)
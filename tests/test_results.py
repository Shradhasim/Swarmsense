import numpy as np

from src.config import SimulationConfig
from src.swarm import Swarm
from src.simulation import Simulation
from src.results import save_results


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

save_results(
    simulation.results,
    "simulation_results.csv"
)

print("Results saved successfully.")
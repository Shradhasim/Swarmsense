
import numpy as np

from config import SimulationConfig
from swarm import Swarm
from simulation import Simulation
from results import save_results


sensing_radii = [1.0, 2.0, 3.0]

for sensing_radius in sensing_radii:

    print(f"Running experiment with sensing radius = {sensing_radius}")

    np.random.seed(42)

    config = SimulationConfig(
        num_robots=20,
        sensing_radius=sensing_radius
    )

    swarm = Swarm(config=config)

    simulation = Simulation(
        swarm=swarm,
        steps=100
    )

    simulation.run()

    filename = f"results/results_sensing_{sensing_radius}.csv"

    save_results(
        simulation.results,
        filename
    )

    print(f"Saved results to {filename}")

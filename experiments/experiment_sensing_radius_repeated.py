
import numpy as np
from pathlib import Path
import csv

from config import SimulationConfig
from swarm import Swarm
from simulation import Simulation


# Project folders
project_folder = Path(__file__).resolve().parent.parent
results_folder = project_folder / "results"

# Experiment settings
sensing_radii = [1.0, 2.0, 3.0]
number_of_runs = 10

# Store summary results
summary_results = []

for sensing_radius in sensing_radii:

    print(f"\nTesting sensing radius: {sensing_radius}")

    for run_number in range(number_of_runs):

        # Different starting conditions for each run
        seed = 42 + run_number
        np.random.seed(seed)

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

        # Extract final measurements
        final_result = simulation.results[-1]

        summary_results.append({
            "sensing_radius": sensing_radius,
            "run": run_number + 1,
            "seed": seed,
            "final_target_distance": final_result["distance_to_target"],
            "average_swarm_spread": np.mean([
                result["average_pairwise_distance"]
                for result in simulation.results
            ]),
            "collision_observations": sum(
                result["collisions"]
                for result in simulation.results
            )
        })

        print(f"  Completed run {run_number + 1}/{number_of_runs}")


# Save all 30 runs
output_file = results_folder / "repeated_experiment_results.csv"

with open(output_file, "w", newline="") as file:

    fieldnames = summary_results[0].keys()

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(summary_results)


print("\nAll experiments completed!")
print(f"Results saved to: {output_file}")


import csv
from pathlib import Path
from statistics import mean, stdev

import matplotlib.pyplot as plt


# Find the project folders
project_folder = Path(__file__).resolve().parent.parent
results_file = project_folder / "results" / "repeated_experiment_results.csv"
output_folder = project_folder / "results"


# Read the experiment results
with open(results_file, "r", newline="") as file:
    reader = csv.DictReader(file)
    data = list(reader)


sensing_radii = [1.0, 2.0, 3.0]

# Metrics to visualize
metrics = {
    "final_target_distance": {
        "title": "Final Distance to Target",
        "ylabel": "Distance",
        "filename": "repeated_target_distance.png"
    },
    "average_swarm_spread": {
        "title": "Average Swarm Spread",
        "ylabel": "Average pairwise distance",
        "filename": "repeated_swarm_spread.png"
    },
    "collision_observations": {
        "title": "Collision Observations",
        "ylabel": "Number of observations",
        "filename": "repeated_collisions.png"
    }
}


# Create one graph for each metric
for metric, settings in metrics.items():

    averages = []
    deviations = []

    for radius in sensing_radii:

        values = [
            float(row[metric])
            for row in data
            if float(row["sensing_radius"]) == radius
        ]

        averages.append(mean(values))
        deviations.append(stdev(values))

    plt.figure(figsize=(8, 5))

    plt.errorbar(
        sensing_radii,
        averages,
        yerr=deviations,
        marker="o",
        capsize=5
    )

    plt.title(settings["title"])
    plt.xlabel("Sensing Radius")
    plt.ylabel(settings["ylabel"])
    plt.xticks(sensing_radii)
    plt.grid(True)

    plt.tight_layout()

    output_file = output_folder / settings["filename"]

    plt.savefig(output_file, dpi=300)
    plt.close()

    print(f"Saved graph: {output_file}")


print("\nAll repeated experiment graphs created!")

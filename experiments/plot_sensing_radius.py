
import csv
from pathlib import Path

import matplotlib.pyplot as plt


project_folder = Path(__file__).resolve().parent.parent
results_folder = project_folder / "results"

sensing_radii = [1.0, 2.0, 3.0]

final_target_distances = []
average_swarm_spreads = []
collision_observations = []

for radius in sensing_radii:

    filename = results_folder / f"results_sensing_{radius}.csv"

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)
        data = list(reader)

    final_target_distances.append(
        float(data[-1]["distance_to_target"])
    )

    average_swarm_spreads.append(
        sum(float(row["average_pairwise_distance"]) for row in data)
        / len(data)
    )

    collision_observations.append(
        sum(int(row["collisions"]) for row in data)
    )


# Graph 1: Final target distance
plt.figure()
plt.plot(sensing_radii, final_target_distances, marker="o")
plt.xlabel("Sensing Radius")
plt.ylabel("Final Target Distance")
plt.title("Effect of Sensing Radius on Mission Performance")
plt.grid(True)
plt.savefig(results_folder / "target_distance.png")
plt.show()


# Graph 2: Average swarm spread
plt.figure()
plt.plot(sensing_radii, average_swarm_spreads, marker="o")
plt.xlabel("Sensing Radius")
plt.ylabel("Average Pairwise Distance")
plt.title("Effect of Sensing Radius on Swarm Spread")
plt.grid(True)
plt.savefig(results_folder / "swarm_spread.png")
plt.show()


# Graph 3: Collision observations
plt.figure()
plt.plot(sensing_radii, collision_observations, marker="o")
plt.xlabel("Sensing Radius")
plt.ylabel("Collision Observations")
plt.title("Effect of Sensing Radius on Collision Observations")
plt.grid(True)
plt.savefig(results_folder / "collisions.png")
plt.show()

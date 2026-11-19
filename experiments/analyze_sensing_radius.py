
import csv
from pathlib import Path
from statistics import mean


# Find the results folder relative to this script.
project_folder = Path(__file__).resolve().parent.parent
results_folder = project_folder / "results"

sensing_radii = [1.0, 2.0, 3.0]

print("\nSENSING RADIUS EXPERIMENT")
print("=" * 75)

print(
    f"{'Radius':<12}"
    f"{'Avg. target distance':<23}"
    f"{'Final target distance':<24}"
    f"{'Avg. swarm spread':<18}"
    f"{'Collision observations':<22}"
)

print("-" * 75)

for radius in sensing_radii:

    filename = results_folder / f"results_sensing_{radius}.csv"

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)
        data = list(reader)

    target_distances = [
        float(row["distance_to_target"]) for row in data
    ]

    swarm_spread = [
        float(row["average_pairwise_distance"]) for row in data
    ]

    collision_observations = [
        int(row["collisions"]) for row in data
    ]

    average_target_distance = mean(target_distances)
    final_target_distance = target_distances[-1]
    average_swarm_spread = mean(swarm_spread)
    total_collision_observations = sum(collision_observations)

    print(
        f"{radius:<12.1f}"
        f"{average_target_distance:<23.3f}"
        f"{final_target_distance:<24.3f}"
        f"{average_swarm_spread:<18.3f}"
        f"{total_collision_observations:<22}"
    )

print("=" * 75)

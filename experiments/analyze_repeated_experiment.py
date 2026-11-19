
import csv
from pathlib import Path
from statistics import mean, stdev


project_folder = Path(__file__).resolve().parent.parent
results_file = project_folder / "results" / "repeated_experiment_results.csv"

# Read experiment data
with open(results_file, "r", newline="") as file:
    reader = csv.DictReader(file)
    data = list(reader)


sensing_radii = [1.0, 2.0, 3.0]

print("\nREPEATED EXPERIMENT ANALYSIS")
print("=" * 95)

for radius in sensing_radii:

    # Select the 10 runs for this sensing radius
    radius_data = [
        row for row in data
        if float(row["sensing_radius"]) == radius
    ]

    target_distances = [
        float(row["final_target_distance"])
        for row in radius_data
    ]

    swarm_spreads = [
        float(row["average_swarm_spread"])
        for row in radius_data
    ]

    collisions = [
        float(row["collision_observations"])
        for row in radius_data
    ]

    print(f"\nSensing radius: {radius}")
    print("-" * 55)

    print(
        f"Final target distance: "
        f"{mean(target_distances):.3f} "
        f"+/- {stdev(target_distances):.3f}"
    )

    print(
        f"Average swarm spread: "
        f"{mean(swarm_spreads):.3f} "
        f"+/- {stdev(swarm_spreads):.3f}"
    )

    print(
        f"Collision observations: "
        f"{mean(collisions):.2f} "
        f"+/- {stdev(collisions):.2f}"
    )

print("\n" + "=" * 95)

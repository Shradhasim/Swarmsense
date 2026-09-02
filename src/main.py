import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import csv

#------ Simulation settings -----

Num_robots = 20
World_size = 10
Num_steps = 100


Sensing_radius = 2.0 # How far the robots can sense other robots
Separation_radius = 0.8 # How close another robot has to be before separation
Separation_strength = 0.20 # How far to separate robots if too close

Alignment_strength = 0.05
Cohesion_strength = 0.01
Max_speed = 0.2
Robot_radius = 0.15

Target_strength = 0.02
Target_stop_radius = 1.0

collision_count = 0
Num_runs = 10
current_run_id = 1
run_finished = False



# ----- Data collection -----
simulation_data = []


# ------Initialize swarm ---------

#Random Start position of robots, There are NUM_ROBOTS rows
def reset_simulation():

    global positions
    global velocities
    global collision_count
    global collision_pairs

    positions = np.random.uniform(
        1,
        World_size - 1,
        size=(Num_robots, 2)
    )

    velocities = np.random.uniform(
        -0.1,
        0.1,
        size=(Num_robots, 2)
    )

    collision_count = 0
    collision_pairs = set()

# Create the first swarm
reset_simulation()

#--------Visulaization ----------
fig, ax = plt.subplots(figsize=(7, 7))

ax.set_xlim(0, World_size)
ax.set_ylim(0, World_size)

ax.set_xlabel("X position")
ax.set_ylabel("Y position")

ax.set_title("Robot Swarm - Separation")

ax.grid(True)

# Target position
Target_position = np.array([
    World_size - 1,
    World_size - 1
])

robot_id = 0

#---- Draw all robots ------
robot_circles = []

for i in range(Num_robots):

    if i == robot_id:
        color = "red"
    else:
        color = "blue"

    circle = Circle(
        positions[i],
        Robot_radius,
        color=color,
        alpha=0.8,
        zorder=2
    )

    ax.add_patch(circle)

    robot_circles.append(circle)

#-----Target-----
target_marker = ax.scatter(
    Target_position[0],
    Target_position[1],
    s=250,
    color="green",
    marker="*",
    label="Target",
    zorder=4 
)

# Draw sensing radius
Sensing_circle = plt.Circle(
    positions[robot_id],
    Sensing_radius,
    color="red",
    fill=False,
    linewidth=2
)

ax.add_patch(Sensing_circle)

# Highlight its neighbors
neighbor_scatter = ax.scatter(
    [],
    [],
    s=180,
    color="orange",
    zorder=3,
    label="Neighbors"
)

# Step counter
step_text = ax.text(
    0.02,
    0.95,
    "",
    transform=ax.transAxes
)

collision_pairs = set()

# ------ Simulation --------

def detect_collisions(positions, Robot_radius):

    collision_pairs = set()
    collision_distance = 2 * Robot_radius

    for i in range(Num_robots):

        for j in range(i + 1, Num_robots):

            difference = positions[i] - positions[j]

            distance = np.linalg.norm(difference)

            

            if distance < collision_distance:

                collision_pairs.add((i, j))

    return collision_pairs

def save_simulation_data(filename= "simulation_data.csv"):
    if not simulation_data:
        print("No simulation data to save.")
        return

    fieldnames = simulation_data[0].keys()

    with open(filename, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(simulation_data)

    print(f"Simulation data saved to {filename}")


def update(frame):

    global positions
    global velocities
    global collision_count
    global collision_pairs
    global current_run_id
    global run_finished

    step = frame % Num_steps

    neighbour_counts= []

    # Prevent duplicate simulation steps
    if step <len(simulation_data):
        return

    #---- Calculate swarm behaviour ---

    for i in range(Num_robots):

        separation = np.zeros(2)
        alignment = np.zeros(2)
        cohesion = np.zeros(2)
        target_force = np.zeros(2)

        neighbors = []

        # Find neighboring robots

        for j in range(Num_robots):

            if i == j:
                continue

            difference = positions[i] - positions[j]
            distance = np.linalg.norm(difference)

            if distance < Sensing_radius:

                neighbors.append(j)

                # ---------------- Separation ----------------

                if 0 < distance < Separation_radius:

                    direction_away = difference / distance
                     # Stronger repulsion when robots are very close
                    strength = ((Separation_radius - distance)/ Separation_radius)
                    separation += direction_away * strength
        

        # Alignment

        if neighbors:

            neighbor_velocities = velocities[neighbors]

            average_velocity = np.mean(
                neighbor_velocities,
                axis=0
            )

            alignment = (
                average_velocity - velocities[i]
            )

        # Cohesion

        if neighbors:

            neighbor_positions = positions[neighbors]

            center_of_neighbors = np.mean(
                neighbor_positions,
                axis=0
            )

            cohesion = (
                center_of_neighbors - positions[i]
            )

        # Target attraction

        direction_to_target = (
            Target_position - positions[i]
        )

        target_distance = np.linalg.norm(
            direction_to_target
        )

        if target_distance > 0:

            if target_distance > Target_stop_radius:
                #Move towards target
                target_force = (
                    direction_to_target / target_distance )
            else:
                #inside the target zone, reducing attraction so robots wont pile directly on the top of the target.
                target_force  = (direction_to_target / target_distance) * 0.2
        else:
            target_force = np.zeros(2)

        # Combine behaviours

        velocity_change = (
            Separation_strength * separation
            + Alignment_strength * alignment
            + Cohesion_strength * cohesion
            + Target_strength * target_force
        )

        velocities[i] += velocity_change

      
        # Limit speed

        speed = np.linalg.norm(velocities[i])

        if speed > Max_speed:

            velocities[i] = (
                velocities[i] / speed
            ) * Max_speed

        #no of neighbour detected by this robot
        neighbour_counts.append(len(neighbors))

    # Calculate average number of neighbors
    average_neighbour_count = np.mean(neighbour_counts)
    # Move robots

    positions = positions + velocities

    # Wall boundry

    for i in range(Num_robots):

        # Left / right walls
        if positions[i, 0] <= 0 or positions[i, 0] >= World_size:

            velocities[i, 0] = -velocities[i, 0]

        # Bottom / top walls
        if positions[i, 1] <= 0 or positions[i, 1] >= World_size:

            velocities[i, 1] = -velocities[i, 1]

    # Keep robots inside the world
    positions[:, 0] = np.clip(
        positions[:, 0],
        0,
        World_size
    )

    positions[:, 1] = np.clip(
        positions[:, 1],
        0,
        World_size
    )

    # Target distance

    distances_to_target = np.linalg.norm(
        positions - Target_position,
        axis=1
    )

    robots_at_target = np.sum(
        distances_to_target < Target_stop_radius
    )

    average_target_distance = np.mean(
        distances_to_target
    )

    minimum_target_distance = np.min(
        distances_to_target
    )

    target_reached = minimum_target_distance < Target_stop_radius

    # Minimun robot- distance

    minimum_robot_distance = float("inf")

    for i in range(Num_robots):

        for j in range(i + 1, Num_robots):

            difference = positions[i] - positions[j]

            distance = np.linalg.norm(difference)

            if distance < minimum_robot_distance:

                minimum_robot_distance = distance

    # Swarm dispersion (how tightly the robots are grouped)
    swarm_center = np.mean(positions, axis=0)

    distances_from_center = np.linalg.norm(
        positions - swarm_center,
        axis=1
    )

    average_swarm_spread = np.mean(distances_from_center)

    # Detect Collision

    current_collision_pairs = detect_collisions(
        positions,
        Robot_radius
    )

    # Number of collisions happening RIGHT NOW
    active_collisions = len(
        current_collision_pairs
    )

    # New collision events
    new_collisions = (
        current_collision_pairs - collision_pairs
    )

    # Add new collision events to total
    collision_count += len(new_collisions)

    # Print new collisions
    for pair in new_collisions:

        i, j = pair

        distance = np.linalg.norm(
            positions[i] - positions[j]
        )

        print(
            f"Collision: Robot {i} <-> Robot {j} | "
            f"Distance: {distance:.3f}"
        )

    # Remember collisions for next frame
    collision_pairs = current_collision_pairs

    # Average speed

    average_speed = np.mean(
        np.linalg.norm(
            velocities,
            axis=1
        )
    )

    # Save data for Analysis

    simulation_data.append({

        "run_id": current_run_id,
        "step": step,
        "target_distance": average_target_distance,
        "minimum_target_distance": minimum_target_distance,
        "minimum_robot_distance": minimum_robot_distance,
        "active_collisions": active_collisions,
        "total_collisions": collision_count,
        "average_speed": average_speed,
        "average_neighbour_count": average_neighbour_count,
        "average_swarm_spread": average_swarm_spread,
        "target_reached": target_reached,
        "robots_at_target": int(robots_at_target)
    })

    # Printing simulation info

    if step % 10 == 0:

        print(
            f"Step {step} | "
            f"Target distance: "
            f"{average_target_distance:.3f} | "
            f"Minimum target distance: "
            f"{minimum_target_distance:.3f} | "
            f"Active collisions: "
            f"{active_collisions} | "
            f"Total collisions: "
            f"{collision_count}"
        )

    # Find neighbour of robot 0

    robot_position = positions[robot_id]

    neighbors = []
    neighbor_distances = []

    for i in range(Num_robots):

        if i == robot_id:
            continue

        difference = (
            positions[i] - robot_position
        )

        distance = np.linalg.norm(
            difference
        )

        if distance < Sensing_radius:

            neighbors.append(i)

            neighbor_distances.append(
                float(distance)
            )

    # Update visalization

    # Update robot positions
    for i in range(Num_robots):

        robot_circles[i].center = positions[i]

    # Update sensing circle
    Sensing_circle.center = positions[robot_id]

    # Update neighbor visualization
    if neighbors:

        neighbor_positions = positions[neighbors]

        neighbor_scatter.set_offsets(
            neighbor_positions
        )

    else:

        neighbor_scatter.set_offsets(
            np.empty((0, 2))
        )

    # Update info

    step_text.set_text(
        f"Step: {step} | "
        f"Active collisions: {active_collisions} | "
        f"Total collisions: {collision_count}"
    )

    # Print Robot 0 info

    if step % 25 == 0:

        print(
            f"Step {step} | "
            f"Robot 0 neighbors: {neighbors}"
        )

        print(
            f"Distances: {neighbor_distances}"
        )

    # return

    

    if step == Num_steps -1 :
        print(
            f" Run {current_run_id} finished."
        )
        if current_run_id < Num_runs:
            current_run_id += 1
            print(
                f"Starting Run {current_run_id}..."
            )
            reset_simulation()

    return (
        *robot_circles,
        Sensing_circle,
        neighbor_scatter,
        step_text
    )

# ------animation---------
animation = FuncAnimation(
    fig,
    update,
    frames=Num_steps,
    interval=50,
    blit=False
)
plt.legend()

plt.show()

save_simulation_data()

# plotting simulation results

steps = [row["step"] for row in simulation_data]

target_distances =[
    row["target_distance"]
    for row in simulation_data
]

swarm_spread =[
    row["average_swarm_spread"]
    for row in simulation_data
]

robots_at_target =[
    row["robots_at_target"]
    for row in simulation_data
]

# ----- Plot 1: Target distance -----
plt.figure(figsize=(8, 5))

plt.plot(
    steps,
    target_distances,
    color="blue"
)

plt.xlabel("Step")
plt.ylabel("Average target distance")
plt.title("Swarm Distance to Target")

plt.grid(True)
plt.tight_layout()
plt.show()


# ----- Plot 2: Swarm spread -----

plt.figure(figsize=(8, 5))

plt.plot(
    steps,
    swarm_spread,
    color="orange"
)

plt.xlabel("Step")
plt.ylabel("Average swarm spread")
plt.title("Swarm Cohesion")

plt.grid(True)
plt.tight_layout()
plt.show()


# ----- Plot 3: Robots at target -----

plt.figure(figsize=(8, 5))

plt.plot(
    steps,
    robots_at_target,
    color="green"
)

plt.xlabel("Step")
plt.ylabel("Number of robots")
plt.title("Robots Reaching Target")

plt.grid(True)
plt.tight_layout()
plt.show()
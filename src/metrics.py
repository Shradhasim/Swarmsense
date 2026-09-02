import numpy as np


def average_pairwise_distance(swarm):

    # Calculates the average distance between all pairs of robots.
    

    distances = []

    for i in range(swarm.num_robots):

        for j in range(i + 1, swarm.num_robots):

            robot_a = swarm.robots[i]
            robot_b = swarm.robots[j]

            distance = np.linalg.norm(
                robot_a.position - robot_b.position
            )

            distances.append(distance)

    if not distances:
        return 0.0

    return float(np.mean(distances))


def distance_to_target(swarm):
    
    # Calculates the average distance of robots to the target.
    

    distances = []

    for robot in swarm.robots:

        distance = np.linalg.norm(
            robot.position - swarm.target_position
        )

        distances.append(distance)

    return float(np.mean(distances))


def target_reached(swarm):
    # Return True when the swarm is sufficiently close to the target.
    

    distance = distance_to_target(swarm)

    return distance <= swarm.config.target_stop_radius
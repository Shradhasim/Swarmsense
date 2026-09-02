import numpy as np


#Calculating the separation force for one robot:  the robot moves away from the nearby robots that are closer than the separation radius
def separation(position, neighbour_positions, separation_radius):
    
    force = np.zeros(2)
    for neighbour_position in neighbour_positions:
        difference = position - neighbour_position #shows which direction is away from the neighbour
        distance = np.linalg.norm(difference) # asks how far away is the neighbour

        if 0 < distance < separation_radius: # only react when neighbour is close enough
            direction_away = difference /distance
            strength = (
                (separation_radius - distance)/ separation_radius
            )
            force += direction_away * strength  # take the robot away from the neighbour
    return force

# Calculating alignment force for one robot: the robot tries to match the average velociy of its nerby neighbours
def alignment(velocity, neighbour_velocities):
    if len(neighbour_velocities) == 0:
        return np.zeros(2)

    average_velocity = np.mean(
        neighbour_velocities,
        axis=0
    )

    force = average_velocity - velocity

    return force


   
    #calculating the cohesion force for one robot : The robot moves toward the average position of its nearby neighbors.
    
def cohesion(position, neighbor_positions):
 
    if len(neighbor_positions) == 0:
        return np.zeros(2)

    center_of_neighbors = np.mean(
        neighbor_positions,
        axis=0
    )

    force = center_of_neighbors - position

    return force


# Calculate the force that moves a robot toward the target.
def target_attraction(position, target_position, target_stop_radius):
    
    direction_to_target = target_position - position

    target_distance = np.linalg.norm(
        direction_to_target
    )

    if target_distance == 0:
        return np.zeros(2)

    if target_distance > target_stop_radius:

        force = (
            direction_to_target
            / target_distance
        )

    else:

        force = (
            direction_to_target
            / target_distance
        ) * 0.2

    return force
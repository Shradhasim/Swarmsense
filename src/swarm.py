import numpy as np

from robot import Robot
from behaviours import (separation, alignment, cohesion, target_attraction,)
from config import SimulationConfig


class Swarm:
   #Represents a collection of autonomous robots.
    

    def __init__(
        self,
        config = None,
        target_position =  None,
    ):
        if config is None:
            config = SimulationConfig()

        self.config = config

        self.num_robots = config.num_robots
        self.world_size = config.world_size
        self.sensing_radius = config.sensing_radius
        self.robot_radius = config.robot_radius

        if target_position is None:
            self.target_position = np.array(
                [config.world_size -1, config.world_size -1],
                dtype= float
            )
        else:
            self.target_position = np.array(
                target_position,
                dtype=float
            )

        self.robots = []

        self.create_robots()

    def create_robots(self):
       
        # crearting robots at random positions with random initial velocities.
    

        self.robots = []

        for robot_id in range(self.num_robots): # Repeat this for every robot

            position = np.random.uniform(
                1,
                self.world_size - 1,
                size=2
            )

            velocity = np.random.uniform(
                -0.1,
                0.1,
                size=2
            )

            robot = Robot(
                robot_id=robot_id,
                position=position,
                velocity=velocity,
                radius=self.robot_radius,
            )

            self.robots.append(robot)

    def get_neighbors(self, robot):
        
       # Find all robots within the sensing radius of the given robot.

        neighbors = []

        for other_robot in self.robots:

            if other_robot.id == robot.id:
                continue

            difference = (
                robot.position
                - other_robot.position
            )

            distance = np.linalg.norm(difference)

            if distance < self.sensing_radius:
                neighbors.append(other_robot)

        return neighbors

    def count_collisions(self):
        # Count the number of robot pairs that are colliding.

        collision_count = 0

        for i in range(self.num_robots):

            for j in range(i + 1, self.num_robots):

                robot_a = self.robots[i]
                robot_b = self.robots[j]

                difference = (
                    robot_a.position
                    - robot_b.position
                )

                distance = np.linalg.norm(
                    difference
                )

                collision_distance = (
                    robot_a.radius
                    + robot_b.radius
                )

                if distance < collision_distance:
                    collision_count += 1

        return collision_count

    # Performing one simulation step using separation, alignment and cohesion. 
    def step(self):
         velocity_changes = []

         for robot in self.robots:
            #find neighbours
            neighbors = self.get_neighbors(robot)

            #neighbour positions
            if neighbors:

                neighbor_positions = np.array(
                    [neighbor.position for neighbor in neighbors]
                )

            else:

                neighbor_positions = np.empty((0, 2))

            #neighbour velocities
            if neighbors:

                neighbor_velocities = np.array(
                    [neighbor.velocity for neighbor in neighbors]
                )

            else:

                neighbor_velocities = np.empty((0, 2))

            #Separation
            separation_force = separation(
                robot.position,
                neighbor_positions,
                separation_radius=self.config.separation_radius,
            )

            #Alignment
            alignment_force = alignment(
                robot.velocity,
                neighbor_velocities,
            )

            #cohesion
            cohesion_force = cohesion(
                robot.position,
                neighbor_positions,
            )

            #target attraction
            target_force = target_attraction(
                robot.position,
                self.target_position,
                target_stop_radius= self.config.target_stop_radius,
            )

            #Combine behaviours

            velocity_change = (
                self.config.separation_strength * separation_force
                + self.config.alignment_strength *alignment_force
                + self.config.cohesion_strength * cohesion_force
                + self.config.target_strength * target_force
            )

            velocity_changes.append(
                velocity_change
            )

        # Update velocities after calculating all forces.
         for robot, velocity_change in zip(
            self.robots,
            velocity_changes
        ):

            robot.update_velocity(
                velocity_change,
                self.config.max_speed
            )

        # Move all robots.
         for robot in self.robots:
            robot.move()
            robot.enforce_boundaries(
                self.world_size )

    
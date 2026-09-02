import numpy as np


class Robot:
# Represents one autonomous robot in the swarm.
    

    def __init__(
        self,
        robot_id,
        position,
        velocity,
        radius=0.15,
    ):
        self.id = robot_id

        self.position = np.array(
            position,
            dtype=float
        )

        self.velocity = np.array(
            velocity,
            dtype=float
        )

        self.radius = radius


    #Update the robot's velocity and limit its maximum speed.
    def update_velocity(self, velocity_change, max_speed):
        self.velocity += velocity_change

        speed = np.linalg.norm(self.velocity)

        if speed > max_speed:
            self.velocity = (
                self.velocity / speed
            ) * max_speed
            
    def move(self):
    # Move the robot according to its current velocity.
        
        self.position += self.velocity

    def enforce_boundaries(self, world_size):
        
        # Keep the robot inside the simulation world. doesnt let the coordinate go below 0 or above the world size

        self.position = np.clip(
            self.position,
            0,
            world_size,
        )
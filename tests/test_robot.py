import sys

sys.path.append("src")

from robot import Robot


robot = Robot(
    robot_id=0,
    position=[9.9, 5],
    velocity=[1.0, 0],
)

print("Robot ID:", robot.id)
print("Position:", robot.position)
print("Velocity:", robot.velocity)

robot.move()
print("Before boundary:", robot.position)

robot.enforce_boundaries( world_size=10)

print("After boundary:", robot.position)

print("Position after moving:", robot.position)

robot.update_velocity(
    velocity_change=[0.1, 0.1],
    max_speed=0.2
)

print("Updated velocity:", robot.velocity)
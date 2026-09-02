from dataclasses import dataclass


@dataclass
class SimulationConfig:
    #Configuration parameters for a SwarmSense simulation.

    num_robots: int = 20
    world_size: float = 10.0

    sensing_radius: float = 2.0
    robot_radius: float = 0.15

    separation_radius: float = 0.8

    separation_strength: float = 0.20
    alignment_strength: float = 0.05
    cohesion_strength: float = 0.01
    target_strength: float = 0.05

    target_stop_radius: float = 0.5

    max_speed: float = 0.2
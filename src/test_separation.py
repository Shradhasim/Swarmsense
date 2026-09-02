import sys

sys.path.append("src")

import numpy as np

from behaviours import (
    separation,
    alignment,
    cohesion,
    target_attraction
)


# -------------------------
# Test separation
# -------------------------

robot = np.array([5.0, 5.0])

neighbors = np.array([
    [5.5, 5.0]
])

force = separation(
    robot,
    neighbors,
    separation_radius=1.0
)

print("Separation:", force)


# -------------------------
# Test alignment
# -------------------------

velocity = np.array([1.0, 0.0])

neighbor_velocities = np.array([
    [0.0, 1.0],
    [0.0, 1.0]
])

force = alignment(
    velocity,
    neighbor_velocities
)

print("Alignment:", force)


# -------------------------
# Test cohesion
# -------------------------

neighbors = np.array([
    [7.0, 5.0],
    [7.0, 7.0]
])

force = cohesion(
    robot,
    neighbors
)

print("Cohesion:", force)


# -------------------------
# Test target attraction
# -------------------------

target = np.array([8.0, 5.0])

force = target_attraction(
    robot,
    target,
    target_stop_radius=1.0
)

print("Target attraction:", force)
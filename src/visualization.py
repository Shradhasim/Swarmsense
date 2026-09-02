import matplotlib.pyplot as plt


class SwarmVisualizer:

    #Visualizes a SwarmSense simulation.

    def __init__(self, swarm):
        self.swarm = swarm

        self.figure, self.axis = plt.subplots()

        self.axis.set_xlim(
            0,
            swarm.world_size
        )

        self.axis.set_ylim(
            0,
            swarm.world_size
        )

        self.axis.set_aspect("equal")

        self.axis.set_title(
            "SwarmSense"
        )

    def draw(self):
        
       # Draw the current swarm state.
        

        self.axis.clear()

        self.axis.set_xlim(
            0,
            self.swarm.world_size
        )

        self.axis.set_ylim(
            0,
            self.swarm.world_size
        )

        self.axis.set_aspect("equal")

        # Draw robots
        for robot in self.swarm.robots:

            self.axis.plot(
                robot.position[0],
                robot.position[1],
                "bo",
            )

        # Draw target
        self.axis.plot(
            self.swarm.target_position[0],
            self.swarm.target_position[1],
            "r*",
            markersize=12,
        )

        self.axis.set_title(
            "SwarmSense"
        )

        plt.pause(0.01)
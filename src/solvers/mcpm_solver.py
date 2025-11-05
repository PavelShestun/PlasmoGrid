import numpy as np
from scipy.ndimage import gaussian_filter

class MCPMSolver:
    """
    Implements the Monte Carlo Physarum Machine (MCPM), a stochastic,
    agent-based model for network formation.
    """
    def __init__(self, grid_size=(100, 100), num_agents=1000, sensing_angle=np.pi/4, sensing_distance=5, sampling_exponent=1.0):
        self.grid_size = grid_size
        self.num_agents = num_agents
        self.sensing_angle = sensing_angle
        self.sensing_distance = sensing_distance
        self.sampling_exponent = sampling_exponent

        # Initialize agent positions and headings
        self.agents = {
            'positions': np.random.rand(num_agents, 2) * grid_size,
            'headings': np.random.rand(num_agents) * 2 * np.pi
        }

        # Initialize deposit and trace fields
        self.deposit_field = np.zeros(grid_size)
        self.trace_field = np.zeros(grid_size)

    def run_simulation(self, num_iterations, diffusion_sigma=1.0, decay_factor=0.95):
        """
        Run the full simulation for a number of iterations.
        """
        for i in range(num_iterations):
            self._propagate()
            self._relax(diffusion_sigma, decay_factor)
            print(f"Iteration {i+1}/{num_iterations} complete.")

    def _propagate(self):
        """
        Move agents based on the deposit field.
        """
        for i in range(self.num_agents):
            pos = self.agents['positions'][i]
            heading = self.agents['headings'][i]

            # Sensing phase
            new_heading = heading + (np.random.rand() - 0.5) * 2 * self.sensing_angle

            # Get values from deposit field at current and new heading
            d0_pos = self._get_sensing_pos(pos, heading)
            d1_pos = self._get_sensing_pos(pos, new_heading)

            d0 = self.deposit_field[int(d0_pos[0]), int(d0_pos[1])]
            d1 = self.deposit_field[int(d1_pos[0]), int(d1_pos[1])]

            # Branching phase (mutation probability)
            p_mut = (d1**self.sampling_exponent) / (d0**self.sampling_exponent + d1**self.sampling_exponent + 1e-9)

            if np.random.rand() < p_mut:
                self.agents['headings'][i] = new_heading

            # Update phase
            new_pos = self._get_sensing_pos(pos, self.agents['headings'][i])
            self.agents['positions'][i] = new_pos

            # Leave a trace
            px, py = int(new_pos[0]), int(new_pos[1])
            self.deposit_field[px, py] += 1
            self.trace_field[px, py] += 1

    def _relax(self, diffusion_sigma, decay_factor):
        """
        Apply diffusion and decay to the fields.
        """
        self.deposit_field = gaussian_filter(self.deposit_field, sigma=diffusion_sigma)
        self.deposit_field *= decay_factor
        self.trace_field *= decay_factor

    def _get_sensing_pos(self, pos, heading):
        """
        Calculate the position to sense, handling boundary conditions.
        """
        new_pos_x = pos[0] + self.sensing_distance * np.cos(heading)
        new_pos_y = pos[1] + self.sensing_distance * np.sin(heading)

        # Periodic boundary conditions (torus)
        new_pos_x = new_pos_x % self.grid_size[0]
        new_pos_y = new_pos_y % self.grid_size[1]

        return np.array([new_pos_x, new_pos_y])

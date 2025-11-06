import numpy as np
from scipy.ndimage import gaussian_filter

class MCPMSolver:
    """
    Implements the Monte Carlo Physarum Machine in continuous space.

    This version models agents moving in a continuous 2D space. They deposit
    a chemoattractant onto a discrete grid (deposit_field), which in turn
    guides their stochastic movement.

    Attributes:
        bounds (tuple): The size of the continuous space, e.g., (100.0, 100.0).
        grid_resolution (int): The resolution of the underlying grid for the deposit field.
        num_agents (int): The number of agents in the simulation.
        agents (dict): A dictionary storing agents' 'positions' and 'headings'.
        deposit_field (np.array): The discrete grid storing chemoattractant levels.
        trace_field (np.array): A grid for visualizing agent paths.
        food_sources (list): A list of dynamic food sources.
    """
    def __init__(self, bounds=(100.0, 100.0), grid_resolution=100, num_agents=1000,
                 sensing_angle=np.pi/4, sensing_distance=5.0, sampling_exponent=1.0):
        self.bounds = np.array(bounds)
        self.grid_resolution = grid_resolution
        self.num_agents = num_agents
        self.sensing_angle = sensing_angle
        self.sensing_distance = sensing_distance
        self.sampling_exponent = sampling_exponent

        self.agents = {
            'positions': np.random.rand(num_agents, 2) * self.bounds,
            'headings': np.random.rand(num_agents) * 2 * np.pi
        }

        self.deposit_field = np.zeros((grid_resolution, grid_resolution))
        self.trace_field = np.zeros((grid_resolution, grid_resolution))
        self.food_sources = []

    def run_simulation(self, num_iterations, diffusion_sigma=1.0, decay_factor=0.95):
        """Runs the full simulation for a number of iterations."""
        for i in range(num_iterations):
            self._propagate()
            self._update_food_sources()
            self._relax(diffusion_sigma, decay_factor)
            if (i+1) % 10 == 0:
                print(f"Iteration {i+1}/{num_iterations} complete.")

    def _world_to_grid(self, coords):
        """Converts continuous world coordinates to discrete grid indices."""
        return np.floor(coords * (self.grid_resolution / self.bounds)).astype(int)

    def _propagate(self):
        """Moves agents based on the deposit field."""
        for i in range(self.num_agents):
            pos = self.agents['positions'][i]
            heading = self.agents['headings'][i]

            # Sensing phase
            new_heading = heading + (np.random.rand() - 0.5) * 2 * self.sensing_angle

            d0_pos = pos + self.sensing_distance * np.array([np.cos(heading), np.sin(heading)])
            d1_pos = pos + self.sensing_distance * np.array([np.cos(new_heading), np.sin(new_heading)])

            # Get chemoattractant values from the grid
            d0_grid = self._world_to_grid(d0_pos % self.bounds)
            d1_grid = self._world_to_grid(d1_pos % self.bounds)

            d0 = self.deposit_field[d0_grid[0], d0_grid[1]]
            d1 = self.deposit_field[d1_grid[0], d1_grid[1]]

            # Branching phase
            p_mut = (d1**self.sampling_exponent) / (d0**self.sampling_exponent + d1**self.sampling_exponent + 1e-9)

            if np.random.rand() < p_mut:
                self.agents['headings'][i] = new_heading

            # Update phase
            move_dist = self.sensing_distance / 2.0 # Move half the sensing distance
            new_pos = pos + move_dist * np.array([np.cos(self.agents['headings'][i]), np.sin(self.agents['headings'][i])])
            self.agents['positions'][i] = new_pos % self.bounds

            # Leave a trace
            grid_pos = self._world_to_grid(new_pos)
            self.deposit_field[grid_pos[0], grid_pos[1]] += 1
            self.trace_field[grid_pos[0], grid_pos[1]] += 1

    def add_food_source(self, position, strength, lifetime):
        """Adds a dynamic food source."""
        self.food_sources.append({'pos': np.array(position), 'strength': strength, 'lifetime': lifetime})

    def _update_food_sources(self):
        """Updates food sources, adding their strength to the deposit field."""
        active_sources = []
        for food in self.food_sources:
            if food['lifetime'] > 0:
                grid_pos = self._world_to_grid(food['pos'])
                self.deposit_field[grid_pos[0], grid_pos[1]] += food['strength']
                food['lifetime'] -= 1
                active_sources.append(food)
        self.food_sources = active_sources

    def _relax(self, diffusion_sigma, decay_factor):
        """Applies diffusion and decay to the fields."""
        self.deposit_field = gaussian_filter(self.deposit_field, sigma=diffusion_sigma)
        self.deposit_field *= decay_factor
        self.trace_field *= decay_factor

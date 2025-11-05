import numpy as np

class ExploreFuseSolver:
    """
    Implements the Explore-and-Fuse algorithm, a cellular automaton-based
    model for solving Steiner tree problems.
    """
    def __init__(self, grid_size=(100, 100), terminals=None):
        self.grid_size = grid_size
        self.grid = np.zeros(grid_size, dtype=int)
        self.terminals = terminals if terminals is not None else []
        self._initialize_grid()

    def _initialize_grid(self):
        """
        Initialize the grid with individual cells at terminal locations.
        """
        for i, terminal in enumerate(self.terminals):
            self.grid[terminal] = i + 1  # Each terminal starts a new cell

    def run_simulation(self, num_iterations):
        """
        Run the simulation for a number of iterations.
        """
        for _ in range(num_iterations):
            self._expand()
            self._fuse()

    def _expand(self):
        """
        Expand all cells by one layer of neighbors.
        """
        new_grid = self.grid.copy()
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                if self.grid[x, y] > 0:
                    # Check neighbors
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.grid_size[0] and 0 <= ny < self.grid_size[1]:
                                if self.grid[nx, ny] == 0:
                                    new_grid[nx, ny] = self.grid[x, y]
        self.grid = new_grid

    def _fuse(self):
        """
        Fuse cells that have come into contact.
        """
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                if self.grid[x, y] > 0:
                    # Check neighbors for different cell IDs
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.grid_size[0] and 0 <= ny < self.grid_size[1]:
                                neighbor_id = self.grid[nx, ny]
                                if neighbor_id > 0 and neighbor_id != self.grid[x, y]:
                                    # Fuse: replace all instances of the higher ID with the lower ID
                                    id_to_replace = max(self.grid[x, y], neighbor_id)
                                    id_to_keep = min(self.grid[x, y], neighbor_id)
                                    self.grid[self.grid == id_to_replace] = id_to_keep

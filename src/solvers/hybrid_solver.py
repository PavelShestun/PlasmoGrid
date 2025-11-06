from solvers.mcpm_solver import MCPMSolver
from solvers.discrete_solver import DiscreteSolver
from graph import PhysarumGraph
import numpy as np

class HybridSolver:
    """
    Implements a hybrid model combining an agent-based explorer (MCPM)
    and a graph-based optimizer (DiscreteSolver).

    The MCPM agents explore a continuous space, creating a weighted graph
    (active zone) based on their traces. The DiscreteSolver then optimizes
    paths within this dynamically generated graph.

    Attributes:
        explorer (MCPMSolver): The agent-based exploration component.
        optimizer (DiscreteSolver): The graph-based optimization component.
        active_zone (PhysarumGraph): The dynamically generated graph.
    """
    def __init__(self, mcpm_params, discrete_solver_params):
        """
        Initializes the HybridSolver.

        Args:
            mcpm_params (dict): Parameters for the MCPMSolver.
            discrete_solver_params (dict): Parameters for the DiscreteSolver.
        """
        self.explorer = MCPMSolver(**mcpm_params)

        # Optimizer is initialized later, once the graph is generated
        self.discrete_solver_params = discrete_solver_params
        self.optimizer = None
        self.active_zone = PhysarumGraph()

    def run_simulation(self, num_iterations):
        """
        Runs the full hybrid simulation cycle.
        """
        for i in range(num_iterations):
            # 1. Exploration Phase
            self.explorer.run_simulation(num_iterations=1)

            # 2. Graph Generation/Update Phase
            self._update_active_zone()

            # 3. Optimization Phase
            if self.active_zone.number_of_nodes() > 1:
                if self.optimizer is None:
                    # Initialize optimizer on the first valid graph
                    terminals = self._get_terminals_from_food()
                    if len(terminals) >= 2:
                        self.optimizer = DiscreteSolver(self.active_zone, terminals[0], terminals[1], **self.discrete_solver_params)

                if self.optimizer:
                    self.optimizer.graph = self.active_zone # Ensure optimizer uses the latest graph
                    _, flows = self.optimizer.solve()

                    # 4. Feedback Loop
                    self._apply_feedback(flows)

            if (i+1) % 10 == 0:
                print(f"Hybrid Iteration {i+1}/{num_iterations} complete.")

    def _update_active_zone(self):
        """
        Constructs or updates the `active_zone` graph from the explorer's trace field.
        """
        # A simple thresholding method to create the graph
        threshold = 0.1
        self.active_zone.clear()

        # Find active nodes
        nodes = np.argwhere(self.explorer.trace_field > threshold)
        for x, y in nodes:
            self.active_zone.add_node((x, y))

        # Add edges between neighboring active nodes
        for u in self.active_zone.nodes():
            for dx, dy in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                v = (u[0] + dx, u[1] + dy)
                if v in self.active_zone:
                    weight = (self.explorer.trace_field[u] + self.explorer.trace_field[v]) / 2.0
                    self.active_zone.add_edge(u, v, weight=weight)

    def _get_terminals_from_food(self):
        """Identifies the graph nodes closest to the current food sources."""
        terminals = []
        for food in self.explorer.food_sources:
            grid_pos = tuple(self.explorer._world_to_grid(food['pos']))
            if grid_pos in self.active_zone:
                terminals.append(grid_pos)
        return terminals

    def _apply_feedback(self, flows):
        """
        Reinforces the explorer's deposit field based on the optimizer's results.
        """
        for (u, v), flow in flows.items():
            # Add a portion of the flow back to the deposit field
            self.explorer.deposit_field[u] += abs(flow) * 0.1
            self.explorer.deposit_field[v] += abs(flow) * 0.1

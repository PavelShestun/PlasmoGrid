import unittest
import networkx as nx
from src.graph import PhysarumGraph
from src.solvers.discrete_solver import DiscreteSolver

class TestDiscreteSolver(unittest.TestCase):

    def test_smoke_test_solver(self):
        """
        A simple smoke test to ensure the solver runs without crashing.
        """
        edges = [(0, 1, {'weight': 1}), (0, 2, {'weight': 2}),
                 (1, 3, {'weight': 1}), (2, 3, {'weight': 2}),
                 (1, 2, {'weight': 3})]
        graph = PhysarumGraph(edges)

        solver = DiscreteSolver(graph, source_node=0, sink_node=3)

        # Test that it runs for a few iterations without error
        solver.run_simulation(num_iterations=5)

        # Check that conductivities have been updated
        self.assertNotEqual(graph.edges[0, 1]['conductivity'], 1.0)

    def test_t_point_convergence(self):
        """
        Test that the T-Point simulation runs and terminates.
        """
        graph = PhysarumGraph(nx.path_graph(5))
        solver = DiscreteSolver(graph, source_node=0, sink_node=4)
        solver.run_simulation_with_t_point(max_iterations=50)

        # We expect it to converge quickly on a simple path graph
        self.assertLess(len(solver.d_path_lengths), 50)

if __name__ == '__main__':
    unittest.main()

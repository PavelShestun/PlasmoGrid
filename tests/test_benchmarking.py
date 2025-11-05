import unittest
import networkx as nx
from src.benchmarking.task_generator import generate_grid_graph
from src.benchmarking.benchmark_algorithms import mst_steiner_tree_heuristic

class TestBenchmarking(unittest.TestCase):

    def test_generate_grid_graph(self):
        """
        Test the grid graph generator.
        """
        graph = generate_grid_graph(5, 5)
        self.assertEqual(graph.number_of_nodes(), 25)
        self.assertEqual(graph.number_of_edges(), 40)

    def test_mst_heuristic(self):
        """
        Test the MST Steiner tree heuristic.
        """
        graph = generate_grid_graph(4, 4)
        terminals = [(0, 0), (3, 3), (0, 3)]

        steiner_tree = mst_steiner_tree_heuristic(graph, terminals)

        # Check that all terminals are in the tree
        for terminal in terminals:
            self.assertIn(terminal, steiner_tree.nodes())

        # Check that the result is a tree
        self.assertTrue(nx.is_tree(steiner_tree))

if __name__ == '__main__':
    unittest.main()

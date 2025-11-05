import numpy as np
import networkx as nx
from graph import PhysarumGraph

class DiscreteSolver:
    """
    Implements the canonical discrete Physarum solver.

    This solver models the Physarum network as an electrical circuit and iteratively
    finds the optimal path by reinforcing edges with higher flow. It includes
    the T-Point convergence criterion for efficient termination.

    Attributes:
        graph (PhysarumGraph): The graph representing the network.
        source_node: The source node for the flow.
        sink_node: The sink node for the flow.
        flow_rate (float): The total flow injected at the source.
        d_path_lengths (list): A history of D-Path lengths at each iteration.
    """
    def __init__(self, graph: PhysarumGraph, source_node, sink_node, flow_rate=1.0):
        """
        Initializes the DiscreteSolver.

        Args:
            graph (PhysarumGraph): The network to be solved.
            source_node: The starting node of the flow.
            sink_node: The ending node of the flow.
            flow_rate (float): The amount of flow to inject. Defaults to 1.0.
        """
        self.graph = graph
        self.source_node = source_node
        self.sink_node = sink_node
        self.flow_rate = flow_rate
        self.d_path_lengths = []

    def solve(self):
        """
        Calculates pressures and flows for the current state of the network.

        This method constructs a system of linear equations based on Kirchhoff's
        current law and Ohm's law, where conductivity is analogous to electrical
        conductance. The system is solved to find the pressure at each node,
        from which the flow in each edge is calculated.

        Returns:
            tuple: A tuple containing:
                - pressures (dict): A dictionary mapping each node to its pressure.
                - flows (dict): A dictionary mapping each edge to its flow.
        """
        num_nodes = self.graph.number_of_nodes()
        if num_nodes == 0:
            return {}, {}

        node_list = list(self.graph.nodes())
        node_map = {node: i for i, node in enumerate(node_list)}

        L = nx.laplacian_matrix(self.graph, nodelist=node_list, weight='conductivity').toarray()

        L[node_map[self.sink_node], :] = 0
        L[node_map[self.sink_node], node_map[self.sink_node]] = 1

        b = np.zeros(num_nodes)
        b[node_map[self.source_node]] = self.flow_rate
        b[node_map[self.sink_node]] = 0

        try:
            pressures_flat = np.linalg.solve(L, b)
        except np.linalg.LinAlgError:
            pressures_flat = np.linalg.pinv(L) @ b

        pressures = {node: pressures_flat[node_map[node]] for node in node_list}

        flows = {}
        for u, v in self.graph.edges():
            conductivity = self.graph.edges[u, v]['conductivity']
            p_u = pressures.get(u, 0)
            p_v = pressures.get(v, 0)
            flows[(u, v)] = conductivity * (p_u - p_v)

        return pressures, flows

    def find_d_path(self, flows):
        """
        Finds the dominant path (D-Path) from source to sink.

        The D-Path is defined as the path starting from the source and greedily
        following the edge with the maximum flow at each step until the sink
        is reached.

        Args:
            flows (dict): A dictionary of flows for each edge.

        Returns:
            list: A list of nodes representing the D-Path, or None if no path is found.
        """
        path = [self.source_node]
        current_node = self.source_node
        visited = {self.source_node}
        while current_node != self.sink_node:
            neighbors = list(self.graph.neighbors(current_node))
            if not neighbors: return None

            next_node = max(neighbors, key=lambda n: abs(flows.get((current_node, n), 0)))

            if next_node in visited: return None

            path.append(next_node)
            visited.add(next_node)
            current_node = next_node
        return path

    def run_simulation_with_t_point(self, max_iterations=200, t_point_stability=5):
        """
        Runs the simulation until the D-Path length stabilizes (T-Point).

        This method provides an efficient stopping criterion. The simulation stops
        when the length of the dominant path (D-Path) remains constant for a
        specified number of consecutive iterations.

        Args:
            max_iterations (int): The maximum number of iterations to run.
            t_point_stability (int): The number of stable iterations required to declare a T-Point.
        """
        last_d_path_length = -1
        stability_counter = 0

        for i in range(max_iterations):
            pressures, flows = self.solve()
            self.graph.update_conductivities(flows)

            d_path = self.find_d_path(flows)

            if d_path:
                current_d_path_length = sum(self.graph[u][v].get('weight', 1) for u, v in zip(d_path, d_path[1:]))
                self.d_path_lengths.append(current_d_path_length)

                if abs(current_d_path_length - last_d_path_length) < 1e-6:
                    stability_counter += 1
                else:
                    stability_counter = 1

                last_d_path_length = current_d_path_length

                if stability_counter >= t_point_stability:
                    print(f"T-Point reached at iteration {i+1}.")
                    return
            else:
                 self.d_path_lengths.append(None)
                 stability_counter = 0

    def run_simulation(self, num_iterations):
        """
        Runs the simulation for a fixed number of iterations.

        Args:
            num_iterations (int): The number of iterations to run.
        """
        for _ in range(num_iterations):
            _, flows = self.solve()
            self.graph.update_conductivities(flows)

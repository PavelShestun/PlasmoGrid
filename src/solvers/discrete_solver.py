import numpy as np
import networkx as nx
from src.graph import PhysarumGraph

class DiscreteSolver:
    """
    Solves for the flow and pressure in a Physarum network using the
    canonical discrete model, with T-Point convergence criterion.
    """
    def __init__(self, graph: PhysarumGraph, source_node, sink_node, flow_rate=1.0):
        self.graph = graph
        self.source_node = source_node
        self.sink_node = sink_node
        self.flow_rate = flow_rate
        self.d_path_lengths = []

    def solve(self):
        """
        Solves the system of linear equations for pressures and calculates flows.
        """
        num_nodes = self.graph.number_of_nodes()
        if num_nodes == 0:
            return np.array([]), {}

        node_list = list(self.graph.nodes())
        node_map = {node: i for i, node in enumerate(node_list)}

        # Build the matrix for the linear system (Laplacian)
        L = nx.laplacian_matrix(self.graph, nodelist=node_list, weight='conductivity').toarray()

        # Ground one node to make the system solvable
        L[node_map[self.sink_node], :] = 0
        L[node_map[self.sink_node], node_map[self.sink_node]] = 1

        b = np.zeros(num_nodes)
        b[node_map[self.source_node]] = self.flow_rate
        b[node_map[self.sink_node]] = 0 # Ground node

        # Solve for pressures
        try:
            pressures_flat = np.linalg.solve(L, b)
            pressures = {node: pressures_flat[node_map[node]] for node in node_list}
        except np.linalg.LinAlgError:
            # Fallback to pseudoinverse if singular
            pressures_flat = np.linalg.pinv(L) @ b
            pressures = {node: pressures_flat[node_map[node]] for node in node_list}

        # Calculate flows
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
        """
        path = [self.source_node]
        current_node = self.source_node
        while current_node != self.sink_node:
            neighbors = list(self.graph.neighbors(current_node))
            if not neighbors:
                return None # Path not found

            next_node = max(neighbors, key=lambda n: abs(flows.get((current_node, n), 0)))

            if next_node in path:
                return None # Avoid cycles

            path.append(next_node)
            current_node = next_node
        return path

    def run_simulation_with_t_point(self, max_iterations=100, t_point_stability=5):
        """
        Run simulation until the D-Path length stabilizes (T-Point).
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

                if current_d_path_length == last_d_path_length:
                    stability_counter += 1
                else:
                    stability_counter = 0

                last_d_path_length = current_d_path_length

                if stability_counter >= t_point_stability:
                    print(f"T-Point reached at iteration {i+1}.")
                    return
            else:
                 self.d_path_lengths.append(None)


    def run_simulation(self, num_iterations):
        """
        Run the full simulation for a fixed number of iterations.
        """
        for _ in range(num_iterations):
            pressures, flows = self.solve()
            self.graph.update_conductivities(flows)

import numpy as np
import networkx as nx
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import cg
from graph import PhysarumGraph

class DiscreteSolver:
    """
    Implements the canonical discrete Physarum solver with scalability improvements.
    This version uses an iterative linear solver (Conjugate Gradient) and supports
    efficient, "hot" updates to the graph structure, making it suitable for
    dynamic environments.
    """
    def __init__(self, graph: PhysarumGraph, source_node, sink_node, flow_rate=1.0):
        """Initializes the DiscreteSolver and builds the initial linear system."""
        self.graph = graph
        self.source_node = source_node
        self.sink_node = sink_node
        self.flow_rate = flow_rate
        self._build_linear_system()
        self._old_conductivities = {edge: self.graph.edges[edge]['conductivity'] for edge in self.graph.edges()}

    def _build_linear_system(self):
        """Constructs the sparse linear system (Lp = b) from the graph."""
        self.node_list = list(self.graph.nodes())
        self.node_map = {node: i for i, node in enumerate(self.node_list)}

        num_nodes = self.graph.number_of_nodes()
        if num_nodes == 0:
            self.L = csc_matrix((0, 0))
            self.b = np.array([])
            return

        L_sparse = nx.laplacian_matrix(self.graph, nodelist=self.node_list, weight='conductivity').asformat('lil')

        sink_idx = self.node_map[self.sink_node]
        L_sparse[sink_idx, :] = 0
        L_sparse[sink_idx, sink_idx] = 1.0

        self.L = L_sparse.asformat('csc')

        self.b = np.zeros(num_nodes)
        self.b[self.node_map[self.source_node]] = self.flow_rate

    def solve(self):
        """Solves the linear system for pressures and calculates flows."""
        if self.L.shape[0] == 0: return {}, {}

        pressures_flat, info = cg(self.L, self.b)
        if info != 0:
            pressures_flat = np.linalg.pinv(self.L.toarray()) @ self.b

        pressures = {node: pressures_flat[self.node_map[node]] for node in self.node_list}

        flows = {}
        for u, v in self.graph.edges():
            p_u, p_v = pressures.get(u, 0), pressures.get(v, 0)
            flows[(u, v)] = self.graph.edges[u, v]['conductivity'] * (p_u - p_v)

        return pressures, flows

    def run_simulation(self, num_iterations):
        """Runs the simulation for a fixed number of iterations."""
        for _ in range(num_iterations):
            self._hot_update_laplacian()
            pressures, flows = self.solve()
            self.graph.update_conductivities(flows)

    def _hot_update_laplacian(self):
        """Efficiently updates the Laplacian matrix based on conductivity changes."""
        self.L = self.L.asformat('lil')
        for u, v in self.graph.edges():
            edge = (u, v)
            new_cond = self.graph.edges[edge]['conductivity']
            old_cond = self._old_conductivities.get(edge, 0)
            delta = new_cond - old_cond

            if abs(delta) > 1e-9:
                u_idx, v_idx = self.node_map[u], self.node_map[v]
                self.L[u_idx, u_idx] += delta
                self.L[v_idx, v_idx] += delta
                self.L[u_idx, v_idx] -= delta
                self.L[v_idx, u_idx] -= delta

            self._old_conductivities[edge] = new_cond

        sink_idx = self.node_map[self.sink_node]
        self.L[sink_idx, :] = 0
        self.L[sink_idx, sink_idx] = 1.0
        self.L = self.L.asformat('csc')

    def add_edge(self, u, v, **attr):
        """Adds an edge and performs a hot update on the linear system."""
        if not self.graph.has_edge(u, v):
            self.graph.add_edge(u, v, **attr)
            self._build_linear_system() # Rebuild is safest when topology changes
            self._old_conductivities = {edge: self.graph.edges[edge]['conductivity'] for edge in self.graph.edges()}

    def remove_edge(self, u, v):
        """Removes an edge and performs a hot update on the linear system."""
        if self.graph.has_edge(u, v):
            self.graph.remove_edge(u, v)
            self._build_linear_system() # Rebuild is safest
            self._old_conductivities = {edge: self.graph.edges[edge]['conductivity'] for edge in self.graph.edges()}

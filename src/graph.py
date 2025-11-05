import networkx as nx

class PhysarumGraph(nx.Graph):
    """
    A graph class representing the network for a Physarum simulation.

    This class extends networkx.Graph to include functionalities specific to
    the Physarum model, such as handling edge attributes like 'conductivity'
    and 'flow'. It ensures that newly added edges are initialized with
    default Physarum-related attributes.

    Attributes:
        _default_conductivity (float): The default conductivity for new edges.
        _default_weight (float): The default weight (length) for new edges.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the PhysarumGraph.

        Accepts the same arguments as a networkx.Graph. After initialization,
        it iterates through all edges to ensure they have the necessary
        Physarum attributes.
        """
        self._default_conductivity = 1.0
        self._default_weight = 1.0
        super().__init__(*args, **kwargs)
        self._initialize_edges()

    def _initialize_edges(self):
        """
        Initializes or updates all edges to ensure they have Physarum attributes.
        """
        for u, v in self.edges():
            self.edges[u, v].setdefault('conductivity', self._default_conductivity)
            self.edges[u, v].setdefault('flow', 0.0)
            self.edges[u, v].setdefault('weight', self._default_weight)

    def add_edge(self, u_for_edge, v_for_edge, **attr):
        """
        Adds an edge to the graph with default Physarum attributes.

        Args:
            u_for_edge: The first node.
            v_for_edge: The second node.
            **attr: Arbitrary keyword arguments for edge attributes.
        """
        super().add_edge(u_for_edge, v_for_edge, **attr)
        self.edges[u_for_edge, v_for_edge].setdefault('conductivity', self._default_conductivity)
        self.edges[u_for_edge, v_for_edge].setdefault('flow', 0.0)
        self.edges[u_for_edge, v_for_edge].setdefault('weight', self._default_weight)

    def update_conductivities(self, flow_dict):
        """
        Updates the conductivity of each edge based on the calculated flow.

        This method implements the adaptive feedback mechanism of the Physarum
        model. The conductivity update rule is a simplified discrete version
        of the differential equation `dD/dt = f(|Q|) - alpha * D`.

        Args:
            flow_dict (dict): A dictionary mapping each edge tuple (u, v) to
                              the absolute flow value |Q_uv| through it.
        """
        for (u, v), flow in flow_dict.items():
            current_conductivity = self.edges[u, v].get('conductivity', self._default_conductivity)
            # Simplified update rule: D_new = (D_old + |Q|) / 2
            self.edges[u, v]['conductivity'] = (current_conductivity + abs(flow)) / 2.0
            self.edges[u, v]['flow'] = abs(flow)

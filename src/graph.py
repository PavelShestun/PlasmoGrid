import networkx as nx

class PhysarumGraph(nx.Graph):
    """
    A graph class for Physarum simulation, extending networkx.Graph.

    This class adds support for storing and updating Physarum-specific
    attributes on the edges, such as conductivity and flow.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize conductivity and flow for all edges
        for u, v in self.edges():
            self.edges[u, v]['conductivity'] = 1.0
            self.edges[u, v]['flow'] = 0.0
            if 'weight' not in self.edges[u, v]:
                self.edges[u, v]['weight'] = 1.0 # Default weight for length

    def update_conductivities(self, flow_dict):
        """
        Update the conductivities of the edges based on the flow using
        the formula D_new = (|Q| + D_old) / 2.
        """
        for (u, v), flow in flow_dict.items():
            self.edges[u, v]['flow'] = abs(flow)
            self.edges[u, v]['conductivity'] = (abs(flow) + self.edges[u, v]['conductivity']) / 2.0

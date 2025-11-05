import networkx as nx
import matplotlib.pyplot as plt

def visualize_graph(graph, title=""):
    """
    Visualizes the PhysarumGraph using matplotlib.

    The thickness of the edges corresponds to their conductivity.
    """
    pos = nx.spring_layout(graph)

    conductivities = [graph.edges[u, v]['conductivity'] for u, v in graph.edges()]
    # Normalize conductivities for better visualization
    max_conductivity = max(conductivities) if conductivities else 1.0
    widths = [5 * c / max_conductivity for c in conductivities]

    nx.draw(graph, pos, with_labels=True, width=widths)
    plt.title(title)
    plt.show()

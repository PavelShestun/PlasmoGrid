import networkx as nx
from graph import PhysarumGraph

def generate_erdos_renyi_graph(n, p, seed=None):
    """
    Generates a PhysarumGraph based on the Erdős-Rényi model.

    Args:
        n (int): The number of nodes.
        p (float): The probability for edge creation.
        seed (int, optional): Seed for random number generator.

    Returns:
        PhysarumGraph: The generated graph.
    """
    g = nx.erdos_renyi_graph(n, p, seed=seed)
    return PhysarumGraph(g)

def generate_barabasi_albert_graph(n, m, seed=None):
    """
    Generates a PhysarumGraph based on the Barabási-Albert model.

    Args:
        n (int): The number of nodes.
        m (int): Number of edges to attach from a new node to existing nodes.
        seed (int, optional): Seed for random number generator.

    Returns:
        PhysarumGraph: The generated graph.
    """
    g = nx.barabasi_albert_graph(n, m, seed=seed)
    return PhysarumGraph(g)

def generate_grid_graph(m, n):
    """
    Generates a 2D grid graph as a PhysarumGraph.

    Args:
        m (int): Number of rows.
        n (int): Number of columns.

    Returns:
        PhysarumGraph: The generated grid graph.
    """
    g = nx.grid_2d_graph(m, n)
    return PhysarumGraph(g)

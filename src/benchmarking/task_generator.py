import networkx as nx
from graph import PhysarumGraph

def generate_erdos_renyi_graph(n, p, seed=None):
    """
    Generates an Erdős-Rényi graph.
    """
    g = nx.erdos_renyi_graph(n, p, seed=seed)
    return PhysarumGraph(g)

def generate_barabasi_albert_graph(n, m, seed=None):
    """
    Generates a Barabási-Albert graph.
    """
    g = nx.barabasi_albert_graph(n, m, seed=seed)
    return PhysarumGraph(g)

def generate_grid_graph(m, n):
    """
    Generates a 2D grid graph.
    """
    g = nx.grid_2d_graph(m, n)
    return PhysarumGraph(g)

def generate_complete_graph(n):
    """
    Generates a complete graph.
    """
    g = nx.complete_graph(n)
    return PhysarumGraph(g)

import networkx as nx
from itertools import combinations

def mst_steiner_tree_heuristic(graph, terminals):
    """
    Finds a Steiner tree using the MST heuristic.

    This heuristic guarantees a solution that is at most twice the optimal length.
    """
    # Create a subgraph induced by the terminal nodes
    subgraph = graph.subgraph(terminals)

    # Find all-pairs shortest paths in the original graph
    paths = dict(nx.all_pairs_dijkstra_path_length(graph))

    # Create a complete graph of terminals with weights as shortest paths
    terminal_graph = nx.Graph()
    for u, v in combinations(terminals, 2):
        terminal_graph.add_edge(u, v, weight=paths[u][v])

    # Find the Minimum Spanning Tree of the terminal graph
    mst = nx.minimum_spanning_tree(terminal_graph)

    # Reconstruct the Steiner tree from the MST edges
    steiner_tree = nx.Graph()
    for u, v in mst.edges():
        path = nx.shortest_path(graph, source=u, target=v)
        nx.add_path(steiner_tree, path)

    return steiner_tree

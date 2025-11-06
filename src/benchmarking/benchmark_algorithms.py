import networkx as nx
from itertools import combinations

def mst_steiner_tree_heuristic(graph, terminals):
    """
    Approximates the Steiner Tree problem using the Minimum Spanning Tree (MST) heuristic.

    This algorithm finds a solution that is guaranteed to be no more than twice the
    cost of the optimal Steiner tree. It works by finding the shortest paths between
    all terminal nodes in the original graph, constructing a complete graph of terminals
    with these path lengths as edge weights, and then finding the MST of this
    complete graph. The final tree is reconstructed from the paths corresponding
    to the edges in the MST.

    Args:
        graph (networkx.Graph): The original graph.
        terminals (list): A list of terminal nodes that must be connected.

    Returns:
        networkx.Graph: A graph representing the approximate Steiner tree.
    """
    if not terminals or len(terminals) < 2:
        return nx.Graph()

    # Create a complete graph of terminals with shortest path distances as weights
    paths = dict(nx.all_pairs_dijkstra_path_length(graph))
    terminal_graph = nx.Graph()
    for u, v in combinations(terminals, 2):
        if u in paths and v in paths[u]:
            terminal_graph.add_edge(u, v, weight=paths[u][v])

    # Find the MST of the complete terminal graph
    mst = nx.minimum_spanning_tree(terminal_graph)

    # Reconstruct the Steiner tree from the paths in the original graph
    steiner_tree = nx.Graph()
    for u, v in mst.edges():
        path = nx.shortest_path(graph, source=u, target=v, weight='weight')
        nx.add_path(steiner_tree, path)

    return steiner_tree

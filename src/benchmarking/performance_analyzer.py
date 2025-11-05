import time
import networkx as nx
import matplotlib.pyplot as plt

def calculate_solution_cost(graph):
    """
    Calculates the total weight of the edges in a graph.
    Assumes edge weights are stored in the 'weight' attribute.
    If 'weight' is not present, it considers the cost as the number of edges.
    """
    if nx.get_edge_attributes(graph, 'weight'):
        return graph.size(weight='weight')
    else:
        return graph.size()

def run_and_analyze(solver_class, graph, solver_args, num_iterations):
    """
    Runs a solver and measures its performance (time and solution cost).
    """
    start_time = time.time()

    solver = solver_class(graph, **solver_args)
    solver.run_simulation(num_iterations)

    end_time = time.time()

    # This is a simplified way to get the result from the discrete solver.
    # In a real scenario, we would have a more robust way to extract the final graph.
    result_graph = solver.graph

    cost = calculate_solution_cost(result_graph)
    execution_time = end_time - start_time

    return cost, execution_time

def plot_comparison(results):
    """
    Plots a bar chart comparing the performance of different algorithms.
    'results' should be a dictionary like:
    {'Algorithm Name': {'cost': 123, 'time': 4.56}}
    """
    labels = results.keys()
    costs = [r['cost'] for r in results.values()]
    times = [r['time'] for r in results.values()]

    x = range(len(labels))
    width = 0.35

    fig, ax1 = plt.subplots()

    ax1.bar(x, costs, width, label='Cost')
    ax1.set_ylabel('Solution Cost')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)

    ax2 = ax1.twinx()
    ax2.bar([i + width for i in x], times, width, label='Time (s)', color='red')
    ax2.set_ylabel('Execution Time (s)')

    fig.tight_layout()
    plt.title('Algorithm Performance Comparison')
    plt.show()

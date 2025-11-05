import argparse
import json
import time
import networkx as nx
from graph import PhysarumGraph
from solvers.discrete_solver import DiscreteSolver
from benchmarking.task_generator import generate_grid_graph, generate_erdos_renyi_graph
from benchmarking.benchmark_algorithms import mst_steiner_tree_heuristic
from benchmarking.data_loader import download_string_db_data

def main():
    parser = argparse.ArgumentParser(description="Run Physarum Solver benchmarks.")
    parser.add_argument('task_type', choices=['grid', 'erdos_renyi', 'string_db'], help="Type of task to run.")
    parser.add_argument('--solvers', nargs='+', default=['discrete', 'mst'], help="Solvers to run.")
    parser.add_argument('--output', default='results.json', help="Output file for results.")
    # Add task-specific arguments
    parser.add_argument('--n', type=int, default=25, help="Number of nodes for generated graphs.")
    parser.add_argument('--p', type=float, default=0.2, help="Probability for Erdos-Renyi graph.")
    parser.add_argument('--organism', default='511145', help="Organism ID for STRING-DB.")

    args = parser.parse_args()

    # --- Task Generation ---
    if args.task_type == 'grid':
        graph = generate_grid_graph(int(args.n**0.5), int(args.n**0.5))
        terminals = [(0, 0), (int(args.n**0.5)-1, int(args.n**0.5)-1)]
    elif args.task_type == 'erdos_renyi':
        graph = generate_erdos_renyi_graph(args.n, args.p)
        terminals = [0, args.n-1]
    elif args.task_type == 'string_db':
        graph = download_string_db_data(args.organism)
        # For simplicity, pick two random nodes as terminals
        terminals = list(graph.nodes())[:2]

    # --- Run Solvers ---
    results = {}
    if 'discrete' in args.solvers:
        print("Running Discrete Solver...")
        g = graph.copy()
        solver = DiscreteSolver(g, terminals[0], terminals[1])
        start = time.time()
        solver.run_simulation_with_t_point()
        t = time.time() - start

        # Binarize and calculate cost
        threshold = 0.1
        res_g = PhysarumGraph()
        for u, v, data in g.edges(data=True):
            if data.get('conductivity', 0) > threshold:
                res_g.add_edge(u, v)

        results['discrete'] = {'cost': res_g.size(), 'time': t}

    if 'mst' in args.solvers:
        print("Running MST Heuristic...")
        g = graph.copy()
        start = time.time()
        res_g = mst_steiner_tree_heuristic(g, terminals)
        t = time.time() - start
        results['mst'] = {'cost': res_g.size(), 'time': t}

    # --- Save Results ---
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=4)
    print(f"Results saved to {args.output}")

if __name__ == "__main__":
    main()

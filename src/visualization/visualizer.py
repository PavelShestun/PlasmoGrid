import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML
import plotly.graph_objects as go

def visualize_graph(graph, title=""):
    """
    Visualizes the PhysarumGraph using matplotlib.

    The thickness of the edges corresponds to their conductivity.
    """
    pos = nx.spring_layout(graph)

    conductivities = [graph.edges[u, v].get('conductivity', 1.0) for u, v in graph.edges()]
    # Normalize conductivities for better visualization
    max_conductivity = max(conductivities) if conductivities else 1.0
    widths = [5 * c / max_conductivity for c in conductivities]

    nx.draw(graph, pos, with_labels=True, width=widths)
    plt.title(title)
    plt.show()

def animate_discrete_solver(solver, num_frames):
    """
    Creates an animation of the discrete solver's convergence.
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    pos = nx.spring_layout(solver.graph)

    def update(frame):
        ax.clear()

        # Run one step of the simulation
        solver.run_simulation(num_iterations=1)

        graph = solver.graph
        conductivities = [graph.edges[u, v].get('conductivity', 1.0) for u, v in graph.edges()]
        max_cond = max(conductivities) if conductivities else 1.0
        widths = [5 * c / max_cond for c in conductivities]

        nx.draw(graph, pos, ax=ax, with_labels=True, width=widths)
        ax.set_title(f"Iteration {frame+1}")

    ani = animation.FuncAnimation(fig, update, frames=num_frames, interval=200, repeat=False)
    plt.close(fig) # Prevent duplicate plot
    return HTML(ani.to_jshtml())

def plot_interactive_convergence(d_path_history, title="D-Path Length Convergence"):
    """
    Creates an interactive convergence plot using Plotly.

    Args:
        d_path_history (list): A list of D-Path lengths at each iteration.
        title (str): The title of the plot.
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=list(range(len(d_path_history))),
        y=d_path_history,
        mode='lines+markers',
        name='D-Path Length'
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Iteration",
        yaxis_title="D-Path Length",
        hovermode="x unified"
    )

    fig.show()

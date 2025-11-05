import matplotlib.pyplot as plt
import base64
from io import BytesIO

def generate_markdown_report(task_description, solver_params, results, convergence_plot=None):
    """
    Generates a Markdown report of the experiment.

    Args:
        task_description (str): A description of the task (e.g., graph type, size).
        solver_params (dict): Parameters used for the solver.
        results (dict): A dictionary of performance metrics from plot_comparison.
        convergence_plot (matplotlib.figure): Optional convergence plot figure.

    Returns:
        str: A string containing the Markdown report.
    """
    report = f"# Physarum Solver Experiment Report\n\n"
    report += f"## Task Description\n\n{task_description}\n\n"
    report += f"## Solver Parameters\n\n"
    for key, value in solver_params.items():
        report += f"- **{key}:** {value}\n"
    report += "\n"

    report += "## Performance Results\n\n"
    report += "| Algorithm              | Solution Cost | Execution Time (s) |\n"
    report += "|------------------------|---------------|--------------------|\n"
    for name, metrics in results.items():
        report += f"| {name:<22} | {metrics['cost']:<13.2f} | {metrics['time']:<18.4f} |\n"
    report += "\n"

    # Embed plots if available
    if convergence_plot:
        tmpfile = BytesIO()
        convergence_plot.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        report += "## Convergence Plot\n\n"
        report += f'<img src="data:image/png;base64,{encoded}">\n\n'

    return report

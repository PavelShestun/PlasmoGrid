import argparse
import json
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def generate_report(results_file, output_file):
    """
    Generates a Markdown report from a JSON results file.
    """
    with open(results_file, 'r') as f:
        results = json.load(f)

    # --- Create Plot ---
    labels = results.keys()
    costs = [r['cost'] for r in results.values()]
    times = [r['time'] for r in results.values()]

    fig, ax1 = plt.subplots()
    width = 0.35
    x = range(len(labels))

    ax1.bar(x, costs, width, label='Cost')
    ax1.set_ylabel('Solution Cost')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)

    ax2 = ax1.twinx()
    ax2.bar([i + width for i in x], times, width, label='Time (s)', color='red')
    ax2.set_ylabel('Execution Time (s)')

    fig.tight_layout()
    plt.title('Algorithm Performance Comparison')

    # Save plot to buffer
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    # --- Generate Markdown ---
    report = "# Benchmark Report\n\n"
    report += "## Performance Results\n\n"
    report += "| Algorithm | Cost | Time (s) |\n"
    report += "|---|---|---|\n"
    for name, data in results.items():
        report += f"| {name} | {data['cost']:.2f} | {data['time']:.4f} |\n"

    report += "\n## Comparison Chart\n\n"
    report += f'<img src="data:image/png;base64,{encoded}">\n'

    with open(output_file, 'w') as f:
        f.write(report)
    print(f"Report saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a report from benchmark results.")
    parser.add_argument('results_file', help="JSON file with benchmark results.")
    parser.add_argument('--output', default='report.md', help="Output Markdown file.")
    args = parser.parse_args()
    generate_report(args.results_file, args.output)

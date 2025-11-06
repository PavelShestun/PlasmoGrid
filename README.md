# Physarum-Solver Framework

## Introduction

**Physarum-Solver Framework** is a Python-based software framework for solving NP-hard optimization problems using bio-inspired algorithms based on the slime mold *Physarum polycephalum*. The framework is designed for researchers and developers interested in exploring unconventional optimization techniques and their application to real-world problems, particularly in systems biology.

This framework provides implementations of several key mathematical models of Physarum behavior, along with tools for benchmarking, visualization, and analysis.

## Features

- **Multiple Solver Models**:
- **Hybrid Solver**: A two-level system combining the strengths of agent-based exploration and graph-based optimization.
  - **Explorer (MCPM)**: Agents explore a continuous, dynamic environment.
  - **Optimizer (DiscreteSolver)**: An iterative graph solver optimizes paths on the emergent network discovered by the explorer.
- **Dynamic Adaptation**: Solvers are designed to handle dynamic environments where graphs can change over time.
- **Scalability**: The `DiscreteSolver` uses an iterative conjugate gradient method, making it suitable for larger graphs.
- **Benchmarking Suite**:
  - A task generator for creating various graph types (grid, random, etc.).
  - Implementations of standard heuristics (e.g., MST for Steiner Tree) for comparison.
  - Automated CLI scripts for running benchmarks and generating performance reports.
- **Application-Ready**:
  - A data loader for real-world biological networks from the STRING-DB database.
  - Examples of applying the framework to find signaling pathways in protein-protein interaction networks.
- **Visualization Tools**:
  - Static and animated visualizations of the network optimization process.
  - Interactive plots for detailed analysis (coming soon).

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd physarum-solver-framework
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Install the project in editable mode:**
    This step makes the `src` modules available globally within your environment, which is necessary for the CLI scripts and tests to work correctly.
    ```bash
    pip install -e .
    ```

## Usage

The framework can be used both programmatically through its Python API and via the command line for automated benchmarking.

### Programmatic Usage (Jupyter Notebooks)

The `notebooks/` directory contains a series of Jupyter notebooks that demonstrate how to use each component of the framework:

- `01_simple_test.ipynb`: Basic usage of the `DiscreteSolver`.
- `02_mcpm_test.ipynb`: Demonstration of the `MCPMSolver`.
- ... and so on for all major features.

### Command-Line Interface (CLI)

The framework includes two CLI scripts for automating experiments.

1.  **`run_benchmark.py`**: Runs a benchmark test.
    ```bash
    # Example: Run the discrete solver on a 36-node grid graph
    python src/run_benchmark.py grid --n 36 --solvers discrete --output grid_results.json

    # Example: Run discrete solver vs. MST heuristic on an Erdos-Renyi graph
    python src/run_benchmark.py erdos_renyi --n 50 --p 0.1 --solvers discrete mst --output er_results.json
    ```

2.  **`generate_report.py`**: Generates a Markdown report from the results.
    ```bash
    python src/generate_report.py grid_results.json --output grid_report.md
    ```

## Project Structure

- `src/`: Contains all the core source code.
  - `solvers/`: Implementations of the different Physarum models.
  - `benchmarking/`: Tools for generating tasks, running benchmarks, and loading data.
  - `visualization/`: Functions for creating plots and animations.
  - `reporting/`: Tools for generating reports.
- `tests/`: Unit tests for the framework.
- `notebooks/`: Jupyter notebooks with examples and demonstrations.
- `data/`: Directory for storing local data.
- `requirements.txt`: A list of Python dependencies.
- `setup.py`: The setup script for making the project installable.
- `LICENSE`: The project's license file.
- `README.md`: This file.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

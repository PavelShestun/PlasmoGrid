# setup.py
from setuptools import setup, find_packages

setup(
    name="physarum_solver_framework",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            'run_benchmark=run_benchmark:main',
            'generate_report=generate_report:main',
        ],
    },
    py_modules=['run_benchmark', 'generate_report']
)

import pandas as pd
import requests
import gzip
import io
from src.graph import PhysarumGraph

def download_string_db_data(organism_id='9606', score_threshold=400):
    """
    Downloads and parses protein interaction data from STRING-DB.

    Args:
        organism_id (str): The NCBI taxonomy ID for the organism.
                           Default is '9606' for Homo sapiens.
        score_threshold (int): The minimum interaction score to include.
                               Default is 400 (medium confidence).

    Returns:
        PhysarumGraph: A graph representing the protein interaction network.
    """
    url = f"https://stringdb-static.org/download/protein.links.v12.0/{organism_id}.protein.links.v12.0.txt.gz"

    print(f"Downloading data from {url}...")
    response = requests.get(url)
    response.raise_for_status()

    print("Decompressing and parsing data...")
    gzip_file = io.BytesIO(response.content)
    with gzip.open(gzip_file, 'rt') as f:
        df = pd.read_csv(f, sep=' ', header=0)

    # Filter by score
    df = df[df['combined_score'] >= score_threshold]

    # Create graph
    graph = PhysarumGraph()
    for _, row in df.iterrows():
        graph.add_edge(row['protein1'], row['protein2'], weight=row['combined_score'])

    print(f"Graph created with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges.")
    return graph

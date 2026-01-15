"""Example usage of GRAPHAVALANCHE."""

from graphavalanche import CitationNetwork, MetadataLoader
import pandas as pd

# Load papers from Excel
papers = MetadataLoader.load_excel("papers_adept.xlsx")

# Clean and validate
papers = MetadataLoader.clean_papers(papers)
if MetadataLoader.validate_papers(papers):
    print(f"✓ Loaded {len(papers)} valid papers")
else:
    print("✗ Some papers are missing required fields")
    exit(1)

# Build citation network
network = CitationNetwork(papers)
print("Building citation connections...")
connections = network.build_connections()
print(f"✓ Found {len(connections)} citation connections")

# Build graph
graph = network.build_graph()
print(f"✓ Graph has {len(graph.nodes())} nodes and {len(graph.edges())} edges")

# Get statistics
stats = network.get_stats()
print(f"\nNetwork Statistics:")
print(f"  Nodes: {stats['nodes']}")
print(f"  Edges: {stats['edges']}")
print(f"  Density: {stats['density']:.4f}")

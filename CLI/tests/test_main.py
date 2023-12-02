import pytest
from src.main import load_network_from_csv

# Test for step 1
def test_load_network_from_csv():
    file_path = "CLI/data/example_network.csv"
    network = load_network_from_csv(file_path)

    # Test the presence of nodes and links
    assert 'A' in network
    assert 'B' in network
    assert 'C' in network
    assert 'D' in network
    assert 'E' in network
    assert 'F' in network
    assert 'G' in network
    assert 'H' in network
    assert 'I' in network

    # Test some links
    assert {'end_node': 'B', 'capacity': 10, 'weight': 5} in network['A']
    assert {'end_node': 'A', 'capacity': 10, 'weight': 5} in network['B']

    # Test bi-directionality (symmetrical capacity)
    assert {'end_node': 'A', 'capacity': 10, 'weight': 5} in network['H']
    assert {'end_node': 'H', 'capacity': 10, 'weight': 5} in network['A']
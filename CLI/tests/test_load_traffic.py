import pytest
from CLI.src.resources.load import load_network_traffic_from_csv

def test_load_traffic_from_csv():
    file_path = "CLI/data/example_traffic.csv"
    traffic = load_network_traffic_from_csv(file_path)

    # Test the presence of sources and destinations
    assert 'A' in traffic
    assert 'B' in traffic
    assert 'I' in traffic
    assert 'H' in traffic

    # Test some traffic demands
    assert traffic['A']['E'] == 1
    assert traffic['B']['A'] == 3
    assert traffic['I']['E'] == 2
    assert traffic['H']['D'] == 4
import pytest
from src.network_alorithms import dijkstra, shortest_path
from src.load import load_network_from_csv

def test_shortest_path():
    network = load_network_from_csv("CLI/data/example_network.csv")

    # Test from A to I
    path_a_to_i = shortest_path(network, 'A', 'I')
    assert path_a_to_i == ['A', 'I']

    # Test from B to F
    path_b_to_f = shortest_path(network, 'B', 'F')
    assert path_b_to_f == ['B', 'I', 'G', 'F']

    # Test from G to D
    path_g_to_d = shortest_path(network, 'G', 'D')
    assert path_g_to_d == ['G', 'F', 'D']
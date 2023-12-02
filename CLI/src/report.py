import csv
import networkx as nx

def model_traffic_flow(network, traffic):
    # create a directed graph using networkx to represent the network
    graph = create_network_graph(network)

    # initialize a data structure to store traffic load on each link
    traffic_load = {}

    # iterate over traffic demands
    for source, destinations in traffic.items():
        for destination, demand in destinations.items():
            # find the shortest path using Dijkstra's algorithm
            shortest_path = nx.shortest_path(graph, source=source, target=destination, weight='weight')

            # update traffic load on each link along the path
            update_traffic_load(traffic_load, shortest_path, demand)

    return traffic_load

def generate_report(traffic_load, output_csv):
    report = []

    for link, demand in traffic_load.items():
        start_node, end_node = link
        report.append({
            'start_node': start_node,
            'end_node': end_node,
            'total_demand': demand
        })

    with open(output_csv, mode='w', newline='') as file:
        fieldnames = ['start_node', 'end_node', 'total_demand']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(report)

def create_network_graph(network):
    # create a directed graph using networkx
    graph = nx.DiGraph()

    # add nodes
    for node, links in network.items():
        graph.add_node(node)

    # add edges with weights
    for node, links in network.items():
        for link in links:
            end_node = link['end_node']
            weight = link['weight']
            graph.add_edge(node, end_node, weight=weight)

    return graph

def update_traffic_load(traffic_load, path, demand):
    # update traffic load on each link along the path
    for i in range(len(path) - 1):
        start_node = path[i]
        end_node = path[i + 1]

        link_key = (start_node, end_node)
        traffic_load.setdefault(link_key, 0)
        traffic_load[link_key] += demand
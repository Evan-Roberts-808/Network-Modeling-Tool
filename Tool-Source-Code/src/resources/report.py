import csv
import networkx as nx
from network_algorithms import shortest_path

def model_traffic_flow(network, traffic):
    graph = create_network_graph(network)
    traffic_load = {}

    for source, destinations in traffic.items():
        for destination, demand in destinations.items():
            try:
                shortest_path = nx.shortest_path(graph, source=source, target=destination, weight='weight')
            except nx.NetworkXNoPath:
                # handle the case where there's no path between source and destination
                # consider it as an unroutable demand
                update_traffic_load(traffic_load, [], demand)
                continue

            update_traffic_load(traffic_load, shortest_path, demand)

    return traffic_load

def generate_report(network, traffic_load, output_csv):
    report = []

    for link, demand in traffic_load.items():
        start_node, end_node = link

        # Ensure that start_node and end_node are strings (keys in the network dictionary)
        start_node = str(start_node)
        end_node = str(end_node)

        # Find the dictionary corresponding to the end_node in the list for start_node
        start_node_edges = network[start_node]
        end_node_dict = next(edge for edge in start_node_edges if edge['end_node'] == end_node)

        # Retrieve the weight/capacity of the edge
        capacity = end_node_dict['capacity']

        # Calculate the utilization percentage
        utilization_percentage = (demand / capacity) * 100

        report.append({
            'start_node': start_node,
            'end_node': end_node,
            'total_demand': demand,
            'utilization_percentage': utilization_percentage
        })

    with open(output_csv, mode='w', newline='') as file:
        fieldnames = ['start_node', 'end_node', 'total_demand', 'utilization_percentage']
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
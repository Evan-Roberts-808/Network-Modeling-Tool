import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.widgets import Button, TextBox
from load import load_network_from_csv, load_network_traffic_from_csv
from network_algorithms import shortest_path

def visualize_network(network, traffic):
    G, pos = create_network_graph(network)

    # Set the figsize to control the size of the window
    fig, ax = plt.subplots(figsize=(20, 18))

    nx.draw(G, pos, with_labels=True, font_weight='bold')

    # Add text boxes for user input
    ax_start = plt.axes([0.8, 0.15, 0.1, 0.04])
    ax_end = plt.axes([0.8, 0.1, 0.1, 0.04])
    text_box_start = TextBox(ax_start, 'Start:', initial='A')
    text_box_end = TextBox(ax_end, 'End:', initial='G')

    # Add a button to find the shortest path
    ax_button = plt.axes([0.8, 0.025, 0.1, 0.04])
    button = Button(ax_button, 'Shortest Path', color='lightgoldenrodyellow')
    button.on_clicked(lambda event: on_shortest_path_button_click(network, G, pos, text_box_start, text_box_end, ax))

    # Add a button to visualize traffic
    ax_button_traffic = plt.axes([0.6, 0.025, 0.1, 0.04])
    button_traffic = Button(ax_button_traffic, 'Visualize Traffic', color='lightgoldenrodyellow')
    button_traffic.on_clicked(lambda event: on_visualize_traffic_button_click(network, G, pos, traffic, ax))

    plt.show()

def create_network_graph(network):
    G = nx.DiGraph()

    for node, links in network.items():
        G.add_node(node)

    for node, links in network.items():
        for link in links:
            end_node = link['end_node']
            weight = link['weight']
            G.add_edge(node, end_node, weight=weight)

    # Calculate the initial spring layout
    pos = nx.spring_layout(G)

    return G, pos

def on_shortest_path_button_click(network, graph, pos, text_box_start, text_box_end, ax):
    # Get user input from text boxes
    start_node = text_box_start.text
    end_node = text_box_end.text

    # Find the shortest path
    path = shortest_path(network, start_node, end_node)
    print("Shortest Path:", path)

    # Get all edges in the graph
    all_edges = list(graph.edges)

    # Initialize path edges
    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

    # Draw all non-path edges and nodes
    non_path_edges = [edge for edge in all_edges if edge not in path_edges]

    nx.draw_networkx_nodes(graph, pos=pos, node_color='b', ax=ax)
    nx.draw_networkx_labels(graph, pos=pos, labels=nx.get_node_attributes(graph, 'label'), font_color='k', font_size=8, font_weight='bold', ax=ax)
    nx.draw_networkx_edges(graph, pos=pos, edgelist=non_path_edges, edge_color='k', width=2, ax=ax)

    # Draw shortest path edges and nodes
    nx.draw_networkx_nodes(graph, pos=pos, nodelist=path, node_color='g', ax=ax)
    nx.draw_networkx_edges(graph, pos=pos, edgelist=path_edges, edge_color='g', width=2, ax=ax)

    # Redraw the canvas
    plt.draw()
    plt.pause(0.1)

def on_visualize_traffic_button_click(network, graph, pos, traffic, ax):
    # Get all edges in the graph
    all_edges = list(graph.edges)

    # Draw all non-path edges and nodes
    nx.draw_networkx_nodes(graph, pos=pos, node_color='b', ax=ax)
    nx.draw_networkx_labels(graph, pos=pos, labels=nx.get_node_attributes(graph, 'label'), font_color='k', font_size=8, font_weight='bold', ax=ax)
    nx.draw_networkx_edges(graph, pos=pos, edgelist=all_edges, edge_color='k', width=2, ax=ax)

    for source, destinations in traffic.items():
        for destination, demand in destinations.items():
            try:
                # Find the shortest path for each traffic demand
                path = nx.shortest_path(graph, source=source, target=destination, weight='weight')

                # Get path edges
                path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

                # Visualize traffic on each link
                visualize_traffic(graph, pos, path, path_edges, demand, ax)

            except nx.NetworkXNoPath:
                # Handle the case where there's no path between source and destination
                print(f"No path between {source} and {destination}")

    # Redraw the canvas
    plt.draw()
    plt.pause(0.1)

def visualize_traffic(graph, pos, path, path_edges, demand, ax):
    for link in path_edges:
        # Check if the link is part of the shortest path
        if link in path_edges:
            print('we are in the if statement')
            start_node, end_node = link

            # Calculate the utilization percentage
            capacity = graph[start_node][end_node]['weight']
            utilization = (demand / capacity) * 100

            # Color the link based on utilization
            if utilization > 100:
                edge_color = 'm'  # magenta for over 100% utilization
            elif utilization > 80:
                edge_color = 'y'  # yellow for over 80% utilization
            else:
                edge_color = 'g'  # green for normal utilization

            nx.draw_networkx_edges(graph, pos=pos, edgelist=[(start_node, end_node)], edge_color=edge_color, width=2, ax=ax)

if __name__ == "__main__":
    network = load_network_from_csv('CLI/data/example_network.csv')
    traffic = load_network_traffic_from_csv('CLI/data/example_traffic.csv')
    print('Loaded Traffic:')
    print(traffic)
    visualize_network(network, traffic)

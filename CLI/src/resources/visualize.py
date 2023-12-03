import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.widgets import Button, TextBox
from load import load_network_from_csv
from network_algorithms import shortest_path

def visualize_network(network):
    G, pos = create_network_graph(network)

    # Set the figsize to control the size of the window
    fig, ax = plt.subplots(figsize=(15, 13))

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
    nx.draw_networkx_nodes(graph, pos=pos, nodelist=path, node_color='r', ax=ax)
    nx.draw_networkx_edges(graph, pos=pos, edgelist=path_edges, edge_color='r', width=2, ax=ax)

    # Redraw the canvas
    plt.draw()
    plt.pause(0.1)

if __name__ == "__main__":
    network = load_network_from_csv('CLI/data/example_network.csv')
    visualize_network(network)

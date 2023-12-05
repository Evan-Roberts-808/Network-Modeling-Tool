import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from load import load_network_from_csv, load_network_traffic_from_csv
from network_algorithms import shortest_path

class NetworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Modeling Tool")

        # Load network data
        self.network = load_network_from_csv('CLI/data/example_network.csv')
        self.traffic = load_network_traffic_from_csv('CLI/data/example_traffic.csv')
        # Initialize instance variables
        self.G, self.pos = self.create_network_graph()
        self.ax = None  # Initialize self.ax

        # Initialize UI components
        self.create_widgets()

    def create_widgets(self):
        # Frame for network visualization
        self.network_frame = ttk.Frame(self.root)
        self.network_frame.grid(row=0, column=0, sticky="nsew")

        # Frame for buttons and input fields
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.grid(row=0, column=1, sticky="nsew")

        # Create buttons and input fields
        ttk.Label(self.control_frame, text="Start Node:").grid(row=0, column=0)
        self.start_entry = ttk.Entry(self.control_frame)
        self.start_entry.grid(row=0, column=1)

        ttk.Label(self.control_frame, text="End Node:").grid(row=1, column=0)
        self.end_entry = ttk.Entry(self.control_frame)
        self.end_entry.grid(row=1, column=1)

        ttk.Button(self.control_frame, text="Shortest Path", command=self.show_shortest_path).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self.control_frame, text="Visualize Traffic", command=self.show_traffic).grid(row=3, column=0, columnspan=2, pady=10)

        # Adjust column and row weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Visualize the network on startup
        self.visualize_network()

    def visualize_network(self):
        # Set the figsize to control the size of the window
        fig, self.ax = plt.subplots(figsize=(20, 18))  # Use self.ax as an instance variable

        nx.draw(self.G, self.pos, with_labels=True, font_weight='bold', node_color='b', font_color='white')

        # Embed the Matplotlib plot into the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.network_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_network_graph(self):
        G = nx.DiGraph()

        for node, links in self.network.items():
            G.add_node(node)

        for node, links in self.network.items():
            for link in links:
                end_node = link['end_node']
                weight = link['weight']
                G.add_edge(node, end_node, weight=weight)

        # Calculate the initial spring layout
        pos = nx.spring_layout(G)

        return G, pos

    def show_shortest_path(self):
        start_node = self.start_entry.get()
        end_node = self.end_entry.get()

        # Find the shortest path
        path = shortest_path(self.network, start_node, end_node)
        print("Shortest Path:", path)

        # Clear the current plot
        self.ax.clear()

        # Get all edges in the graph
        all_edges = list(self.G.edges)

        # Initialize path edges
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

        # Draw all non-path edges and nodes
        non_path_edges = [edge for edge in all_edges if edge not in path_edges]

        nx.draw_networkx_nodes(self.G, pos=self.pos, node_color='b', ax=self.ax)
        nx.draw_networkx_labels(self.G, pos=self.pos, labels=nx.get_node_attributes(self.G, 'label'), font_color='w', font_size=10, font_weight='bold', ax=self.ax)
        nx.draw_networkx_edges(self.G, pos=self.pos, edgelist=non_path_edges, edge_color='k', width=2, ax=self.ax)

        # Draw shortest path edges and nodes
        nx.draw_networkx_nodes(self.G, pos=self.pos, nodelist=path, node_color='g', ax=self.ax)
        nx.draw_networkx_labels(self.G, pos=self.pos, labels={node: node for node in self.G.nodes}, font_color='w', font_size=10, font_weight='bold', ax=self.ax)
        nx.draw_networkx_edges(self.G, pos=self.pos, edgelist=path_edges, edge_color='g', width=2, ax=self.ax)

        # Redraw the canvas
        self.ax.figure.canvas.draw()
        plt.pause(0.1)

        # Close the additional figure window
        plt.close('all')

    def show_traffic(self):
        # Get all edges in the graph
        all_edges = list(self.G.edges)

        # Draw all non-path edges and nodes
        nx.draw_networkx_nodes(self.G, pos=self.pos, node_color='b', ax=self.ax)
        nx.draw_networkx_edges(self.G, pos=self.pos, edgelist=all_edges, edge_color='k', width=2, ax=self.ax)

        # Draw node labels
        nx.draw_networkx_labels(self.G, pos=self.pos, labels=nx.get_node_attributes(self.G, 'label'), font_color='k', font_size=8, font_weight='bold', ax=self.ax)

        for source, destinations in self.traffic.items():
            for destination, demand in destinations.items():
                try:
                    # Find the shortest path for each traffic demand
                    path = shortest_path(self.network, source, destination)

                    # Get path edges
                    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

                    # Visualize traffic on each link
                    self.visualize_traffic(path, path_edges, demand)

                except nx.NetworkXNoPath:
                    # Handle the case where there's no path between source and destination
                    print(f"No path between {source} and {destination}")

        # Redraw the canvas
        self.ax.figure.canvas.draw()

        # Close the additional figure window
        plt.close('all')
    
    def visualize_traffic(self, path, path_edges, demand):
        # Color the link based on utilization
        for link in path_edges:
            start_node, end_node = link

            # Calculate the utilization percentage
            capacity = self.G[start_node][end_node]['weight']
            utilization = (demand / capacity) * 100

            # Color the link based on utilization
            if utilization > 100:
                edge_color = 'm'  # magenta for over 100% utilization
            elif utilization > 80:
                edge_color = 'y'  # yellow for over 80% utilization
            else:
                edge_color = 'g'  # green for normal utilization

            nx.draw_networkx_edges(self.G, pos=self.pos, edgelist=[(start_node, end_node)], edge_color=edge_color, width=2, ax=self.ax)

if __name__ == "__main__":
    network = load_network_from_csv('CLI/data/example_network.csv')
    traffic = load_network_traffic_from_csv('CLI/data/example_traffic.csv')
    root = tk.Tk()
    app = NetworkApp(root)
    root.mainloop()

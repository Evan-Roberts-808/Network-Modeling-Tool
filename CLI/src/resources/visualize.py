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

        # Initialize instance variables
        self.G, self.pos = None, None
        self.ax = None  # Initialize self.ax
        self.network = None
        self.traffic = None
        self.network_path = None
        self.traffic_path = None

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
        ttk.Button(self.control_frame, text="Visualize Traffic", command=self.visualize_traffic).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(self.control_frame, text="Import Network", command=self.import_network).grid(row=4, column=0, pady=10)
        ttk.Button(self.control_frame, text="Import Traffic", command=self.import_traffic).grid(row=4, column=1, pady=10)

        # Adjust column and row weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Visualize the network on startup
        self.visualize_network()

    def visualize_network(self):
        if self.G is not None and self.pos is not None:
            # Set the figsize to control the size of the window
            fig, self.ax = plt.subplots(figsize=(20, 18))  # Use self.ax as an instance variable

            nx.draw(self.G, self.pos, with_labels=True, font_weight='bold', node_color='b', font_color='white')

            # Embed the Matplotlib plot into the Tkinter window
            canvas = FigureCanvasTkAgg(fig, master=self.network_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_network_graph(self):
        try:
            G = nx.DiGraph()

            for node, links in self.network.items():
                G.add_node(node)

            for node, links in self.network.items():
                for link in links:
                    end_node = link['end_node']
                    weight = link['weight']
                    capacity = link['capacity']
                    G.add_edge(node, end_node, weight=weight, capacity=capacity)

            # Calculate the initial spring layout
            pos = nx.spring_layout(G)

            return G, pos
        except Exception as e:
            print(f'Could not create graph, self.G is None. Error: {e}')
            return None, None

    def import_network(self):
        file_path = filedialog.askopenfilename(title="Select Network CSV", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.network_path = file_path
            self.update_network()

    def import_traffic(self):
        file_path = filedialog.askopenfilename(title="Select Traffic CSV", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.traffic_path = file_path
            self.update_traffic()

    def update_network(self):
        if self.network_path:
            self.network = load_network_from_csv(self.network_path)
            self.G, self.pos = self.create_network_graph()
            self.visualize_network()

    def update_traffic(self):
        if self.traffic_path:
            self.traffic = load_network_traffic_from_csv(self.traffic_path)
            self.visualize_traffic()

    def show_shortest_path(self):
        if not self.network:
            self.import_network()

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

    def visualize_traffic(self):
        if not self.traffic:
            self.import_traffic()
            
        if self.G is not None and self.pos is not None and hasattr(self, 'traffic'):
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
                        self.visualize_traffic_on_link(path_edges, demand)

                    except nx.NetworkXNoPath:
                        # Handle the case where there's no path between source and destination
                        print(f"No path between {source} and {destination}")

            # Redraw the canvas
            self.ax.figure.canvas.draw()

            # Close the additional figure window
            plt.close('all')

    def visualize_traffic_on_link(self, path_edges, demand):
        if self.G is not None and self.pos is not None:
            # Color the link based on utilization
            for link in path_edges:
                start_node, end_node = link
                # Calculate the utilization percentage
                capacity = self.G[start_node][end_node]['capacity']
                utilization = (demand / capacity) * 100
                print(utilization)

                # Color the link based on utilization
                if utilization > 100:
                    edge_color = 'm'  # magenta for over 100% utilization
                elif utilization > 80:
                    edge_color = 'y'  # yellow for over 80% utilization
                else:
                    edge_color = 'g'  # green for normal utilization

                nx.draw_networkx_edges(self.G, pos=self.pos, edgelist=[(start_node, end_node)], edge_color=edge_color, width=2, ax=self.ax)

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkApp(root)
    root.mainloop()

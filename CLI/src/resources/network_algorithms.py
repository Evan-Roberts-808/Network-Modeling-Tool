import heapq
from load import load_network_from_csv

def dijkstra(network, start_node):
    # Initialize distances and predecessors
    distances = {node: float('inf') for node in network}
    predecessors = {node: None for node in network}
    distances[start_node] = 0

    # Priority queue to store nodes and their distances
    priority_queue = [(0, start_node)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # print(f"Exploring node: {current_node}, Distance: {current_distance}")

        # Explore neighbors
        for link in network[current_node]:
            neighbor = link['end_node']
            weight = link['weight']

            # print(f"Checking neighbor: {neighbor}, Weight: {weight}")

            distance_to_neighbor = current_distance + weight

            # Update distance and predecessor if a shorter path is found
            if distance_to_neighbor < distances[neighbor]:
                distances[neighbor] = distance_to_neighbor
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (distance_to_neighbor, neighbor))

    return distances, predecessors

def shortest_path(network, start_node, end_node):
    distances, predecessors = dijkstra(network, start_node)

    # Reconstruct the shortest path
    path = []
    current_node = end_node
    while current_node is not None:
        path.insert(0, current_node)
        current_node = predecessors[current_node]

    return path

if __name__ == '__main__':
    network = load_network_from_csv('CLI/data/example_network.csv')
    start_node = 'A'
    end_node = 'G'
    
    path = shortest_path(network, start_node, end_node)
    print(path)
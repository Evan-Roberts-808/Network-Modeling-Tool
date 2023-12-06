import pandas as pd

def load_network_from_csv(file_path):
    # read csv into pandas dataframe
    df = pd.read_csv(file_path)

    # convert dataframe into dictionary
    network = {}
    for _, row in df.iterrows():
        start_node = row['Start']
        end_node = row['End']
        capacity = row['Capacity']
        weight = row['Weight']

        # create entries for start and end nodes if they don't exist
        network.setdefault(start_node, []).append({'end_node': end_node, 'capacity': capacity, 'weight': weight})
        network.setdefault(end_node, []).append({'end_node': start_node, 'capacity': capacity, 'weight': weight})

    print('Loaded network:')
    print(network)

    return network

def load_network_traffic_from_csv(file_path):
    df = pd.read_csv(file_path)

    traffic = {}
    for _, row in df.iterrows():
        source_node = row['Source']
        destination_node = row['Destination']
        demand = row['Demand']

        traffic.setdefault(source_node, {})[destination_node] = demand
        
    return traffic

if __name__ == '__main__':
    load_network_from_csv('CLI/data/example_network.csv')
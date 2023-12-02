import pandas as pd
from src.network_alorithms import dijkstra, shortest_path

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

    return network
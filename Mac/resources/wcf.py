from resources.load import load_network_from_csv, load_network_traffic_from_csv
from resources.report import model_traffic_flow

def determine_worst_case_failure(network, traffic):
    worst_case = None

    for link in network:
        modified_network = remove_link(network, link)
        traffic_load = model_traffic_flow(modified_network, traffic)

        analysis_result = analyze_traffic_load(traffic_load)

        if worst_case is None or analysis_result > worst_case[1]:
            worst_case = (link, analysis_result)
    
    return worst_case
    
def remove_link(network, link):
    # modify network to remove specific link
    modified_network = {node: [l for l in links if l['end_node'] != link] for node, links in network.items()}
    return modified_network

def analyze_traffic_load(traffic_load):
    return len([demand for demand in traffic_load.values() if demand > 0])

if __name__ == "__main__":
    network = load_network_from_csv('CLI/data/example_network.csv')
    traffic = load_network_traffic_from_csv('CLI/data/example_traffic.csv')

    worst_case_result = determine_worst_case_failure(network, traffic)

    print("Worst Case Failure:")
    print(f"Link Removed: {worst_case_result[0]}")
    print(f"Un-routable Traffic Demands: {worst_case_result[1]}")
from resources.load import load_network_from_csv, load_network_traffic_from_csv
from resources.report import model_traffic_flow, generate_report

def export_report_csv(network, traffic, output_csv):
    network = load_network_from_csv(network)

    traffic = load_network_traffic_from_csv(traffic)

    traffic_load = model_traffic_flow(network, traffic)

    generate_report(network, traffic_load, output_csv)

if __name__ == "__main__":
    # input paths to network and traffic csvs
    export_report_csv('CLI/data/example_network.csv', 'CLI/data/example_traffic.csv', 'test.csv')
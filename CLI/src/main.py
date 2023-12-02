from load import load_network_from_csv, load_network_traffic_from_csv
from report import model_traffic_flow, generate_report

def main(network, traffic):
    network = load_network_from_csv(network)

    traffic = load_network_traffic_from_csv(traffic)

    traffic_load = model_traffic_flow(network, traffic)

    generate_report(traffic_load, 'report.csv')

if __name__ == "__main__":
    # input paths to network and traffic csvs
    main('CLI/data/example_network.csv', 'CLI/data/example_traffic.csv')
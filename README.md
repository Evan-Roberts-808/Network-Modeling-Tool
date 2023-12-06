# Network-Modeling-Tool Coding Challenge

Welcome to my implementation of a Network Modeling Tool for the Weekly Coding Challenge #38.

<p><b>Note:</b> While using the application, if you find any bugs, please check the issues tab in the repo to see if they've been reported and if not submit an issue. This will help me find bugs in the application and address them.</p>


## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Acknowledgements](#acknowledgements)

## Overview
This project is a powerful tool for modeling and analyzing network traffic. It allows users to import network data, visualize traffic, find the shortest path, and generate detailed reports on network utilization.

## Getting Started

### Running Locally

To run the Network Modeling Tool on your local machine, follow these steps:

1. In your terminal, run the following command:
```
git@github.com:Evan-Roberts-808/Network-Modelling-Tool.git
```

2. Navigate to the "Tool-Source-Code" directory:
```
cd your/path/to/Tool-Source-Code
```

3. Install the required dependencies:
```
pip install -r requirements.txt
```

4. Run the tool using the following command:
```
python src/main.py
```

<b>Notes:</b> 
- Example networks and corresponding traffic data can be found in the <b>Example-Networks</b> directory.

### Running the Executable (Windows)

1. Follow the directions above to clone the repo, or click the green "Code" button and select "Download ZIP". If necessary, unzip the downloaded file.

2. In your file explorer, open the Project folder, and navigate into the nested Windows folder.

3. Run the main.exe executable to run the tool.

<b>Notes:</b> 
- Example networks and corresponding traffic data can be found in the <b>Example-Networks</b> directory.
- Due to it not being a widely distributed executable, your anti virus may stop to scan the file before the tool can be launched.

### Running the Executable (macOS)

1. Follow the directions above to clone the repo, or click the green "Code" button and select "Download ZIP". If necessary, unzip the downloaded file.

2. In your file explorer, open the Project folder, and navigate into the nested Mac folder.

3. Locate the "main" file.

4. Right-click on the "main" file and select "Open." You might encounter a security prompt because the application is from an unidentified developer.

5. To open the application, right-click on it again and select "Open" from the context menu.

6. If the antivirus software on your macOS system flags the application, you may need to allow the application to run. You can do this through the antivirus software settings.

7. Run the "main" executable to use the tool.

<b>Note:</b> 
- Example networks and corresponding traffic data can be found in the <b>Example-Networks</b> directory.
- macOS has strict security measures for applications from unidentified developers, and you might need to override these settings to run the executable.

## Features
- Visualize Network Traffic: Import network data and traffic data to visualize traffic flows with a user-friendly interface.
- Shortest Path Finder: Find the shortest path between two input nodes in the network.
- Generate Reports: Analyze network utilization and generate detailed reports for further insights.

## Technologies used

- Python: The application is primarily developed using Python, a versatile and powerful programming language.

- Networkx: NetworkX is employed for modeling and analyzing the structure of complex networks.

- Matplotlib: Matplotlib is used for creating interactive visualizations of network traffic and utilization.

- Tkinter: The standard GUI toolkit that is included in Python. Used to create our user interface to allow them to interact with the tool.

- pandas: A powerful data manipulation library for Python which we use to read network and traffic csv files and properly store their data in appropriate data structures to use in the program.

## Acknowledgements
- Original challenge by <a href="https://codingchallenges.substack.com/p/coding-challenge-38-network-modelling?utm_source=post-email-title&publication_id=1483213&post_id=139342658&utm_campaign=email-post-title&isFreemail=true&r=30rz1q&utm_medium=email">Weekly Coding Challenges</a>.
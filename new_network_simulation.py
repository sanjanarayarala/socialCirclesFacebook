import networkx as nx
import matplotlib.pyplot as plt
import random
from nw_model.network import build_network

def network_simulation_analysis_large(graph):
    #Create a copy of the graph to preserve the original
    sim_graph = graph.copy()

    #removing nodes with high betweenness centrality
    centrality = nx.betweenness_centrality(graph)
    high_centrality_nodes = sorted(centrality, key=centrality.get, reverse=True)[:10]
    sim_graph.remove_nodes_from(high_centrality_nodes)
    print(f"Removed high-centrality nodes: {high_centrality_nodes}")

    #Removing multiple random edges
    if len(sim_graph.edges()) > 100:
        edges_to_remove = random.sample(list(sim_graph.edges()), 100)
        sim_graph.remove_edges_from(edges_to_remove)
        print(f"Removed 100 random edges")

    #Adding multiple new nodes with multiple connections
    new_nodes = []
    for i in range(5):
        new_node = max(sim_graph.nodes()) + 1
        new_nodes.append(new_node)
        nodes_to_connect = random.sample(list(sim_graph.nodes()), min(10, len(sim_graph.nodes())))
        sim_graph.add_node(new_node)
        sim_graph.add_edges_from((new_node, node) for node in nodes_to_connect)
    print(f"Added 5 new nodes each connected to 10 existing nodes")

    #Creating a 'super node' connected to many nodes
    super_node = max(sim_graph.nodes()) + 1
    super_connections = random.sample(list(sim_graph.nodes()), min(100, len(sim_graph.nodes())))
    sim_graph.add_node(super_node)
    sim_graph.add_edges_from((super_node, node) for node in super_connections)
    print(f"Added a super node connected to 100 existing nodes")

    #Analyze and plot the original and simulated graphs
    analyze_and_plot(graph, sim_graph)

def analyze_and_plot(original_graph, simulated_graph):
    pos = nx.spring_layout(original_graph) 
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 7))
    plt.subplots_adjust(wspace=0.3)

    # Plot the original graph
    nx.draw(original_graph, pos, ax=axes[0], node_size=50, with_labels=False, font_size=8)
    axes[0].set_title("Original Graph")
    
    #Update positions for new nodes in the simulated graph for consistency
    pos.update(nx.spring_layout(simulated_graph, pos=pos, fixed=pos.keys()))  # Fixed positions for original nodes

    #Plot the simulated graph
    nx.draw(simulated_graph, pos, ax=axes[1], node_size=50, with_labels=False, font_size=8)
    axes[1].set_title("Simulated Graph")

    plt.show()

    print_network_stats(original_graph, "Original graph")
    print_network_stats(simulated_graph, "Simulated graph")

def print_network_stats(graph, name):
    components = nx.number_connected_components(graph)
    if nx.is_connected(graph):
        avg_path_len = nx.average_shortest_path_length(graph)
        print(f"{name} - Number of connected components: {components}, Average path length: {avg_path_len}")
    else:
        print(f"{name} - Number of connected components: {components}, Graph is not connected")


G= build_network() 
network_simulation_analysis_large(G)
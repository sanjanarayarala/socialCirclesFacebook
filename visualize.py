import matplotlib.pyplot as plt
import networkx as nx
from nw_model.network import build_network

def plot(G):
    plt.figure(figsize=(6, 6))
    pos = nx.spring_layout(G, scale=2)  
    nx.draw(G, pos, with_labels=True, node_size=50, node_color='blue', edge_color='gray')
    plt.show()

G= build_network()
plot(G)
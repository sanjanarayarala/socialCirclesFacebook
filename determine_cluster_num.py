#TO find suitable no. of clusters.
import networkx as nx
import os
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
from nw_model.network import build_network

def optimal_clusters(graph, max_clusters=10):
    # Gather feature lists
    feature_list = [list(data['features'].values()) for node, data in graph.nodes(data=True) if 'features' in data]

    #maximum length of any feature list
    max_length = max(len(features) for features in feature_list)

    #Ensure all features are of the same length
    padded_features = [features + [0] * (max_length - len(features)) for features in feature_list]

    features = np.array(padded_features)

    if features.size == 0:
        print("No features available for clustering.")
        return

    inertias = []

    for k in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(features)
        inertias.append(kmeans.inertia_)

    #Plotting the elbow curve for inertia
    plt.figure(figsize=(12, 6))
    plt.plot(range(2, max_clusters + 1), inertias, marker='o')
    plt.title('Elbow Method For Optimal k (Inertia)')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.grid(True)
    plt.show()


G=build_network()
optimal_clusters(G, max_clusters=15) #plot resulted in 6


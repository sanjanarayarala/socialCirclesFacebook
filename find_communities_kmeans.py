import networkx as nx
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
from nw_model.network import build_network

def detect_communities_kmeans(graph, num_clusters=3):
    #Ensure nodes have features and that they are all of same length
    feature_list = []
    nodes = []
    for node, data in graph.nodes(data=True):
        if 'features' in data:
            nodes.append(node)
            feature_list.append(list(data['features'].values()))
    
    #Find the max length of any feature list
    max_length = max(len(features) for features in feature_list)
    padded_features = [features + [0] * (max_length - len(features)) for features in feature_list]
    
    features = np.array(padded_features)
    
    #fit KMeans
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(features)
    labels = kmeans.labels_

    # Compute the most common features for each community
    community_features = {}
    for node, label in zip(nodes, labels):
        graph.nodes[node]['community'] = label
        features = graph.nodes[node]['features']
        if label not in community_features:
            community_features[label] = {}
        for feature, value in features.items():
            if feature not in community_features[label]:
                community_features[label][feature] = []
            community_features[label][feature].append(value)
    
    # For each community, calculate the average of each feature
    for label, features in community_features.items():
        community_features[label] = {feature: np.mean(values) for feature, values in features.items()}
    
    return community_features

def annotate_subgraphs_with_features(graph, community_features, layout=nx.spring_layout):
    #Identify unique communities
    communities = set(nx.get_node_attributes(graph, 'community').values())
    for community in communities:
        #Extract subgraph
        nodes_in_community = [node for node in graph if graph.nodes[node]['community'] == community]
        subgraph = graph.subgraph(nodes_in_community)
        
        #Plot  subgraph
        plt.figure(figsize=(10, 10))
        pos = layout(subgraph)
        nx.draw(subgraph, pos, with_labels=True, node_size=100, font_size=8)
        
        #Annotate with the most common features in this community
        common_features = community_features[community]
        most_common_features = sorted(common_features, key=common_features.get, reverse=True)[:3]  # top 3 features
        text_str = '\n'.join(f'{feature}: {common_features[feature]:.2f}' for feature in most_common_features)
        plt.text(0.05, 0.95, text_str, transform=plt.gca().transAxes, fontsize=12,
                 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))
        
        plt.title(f'Community {community} - Top 3 Features')
        plt.show()


G=build_network() 
community_features= detect_communities_kmeans(G, num_clusters=6)
annotate_subgraphs_with_features(G, community_features)
import networkx as nx
import os
import matplotlib.pyplot as plt


def load_edges(file_path, graph):
    #print(f"Loading edges from {file_path}")
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) != 2:
                continue  # Skip any malformed lines

            node1, node2 = map(int, parts)
            graph.add_edge(node1, node2)  # Adds the edge to the graph

   
    #print(f"Graph now has {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")



def load_features(file_path, graph, is_ego=False):
    feature_names = graph.graph.get('feature_names', {})
    #print(f"Loading features from {file_path}, is_ego={is_ego}")

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) < 2:  # Ensures there's at least one feature plus a node ID
                print("Warning: Malformed line skipped:", line)
                continue

            node_id = int(parts[0])
            features = list(map(int, parts[1:]))

            # Ensures every node mentioned has a node entry in the graph
            if node_id not in graph:
                graph.add_node(node_id)

            # Assigns features to the node
            # Maps feature indices to their descriptive names or defaults to 'feature_index'
            named_features = {feature_names.get(i, f'feature_{i}'): feat for i, feat in enumerate(features)}

            if is_ego:
                # For ego features, combine with existing using max to preserve the most significant features
                current_features = graph.nodes[node_id].get('features', {})
                updated_features = {k: max(current_features.get(k, 0), named_features[k]) for k in named_features}
                graph.nodes[node_id]['features'] = updated_features
            else:
                graph.nodes[node_id]['features'] = named_features
    '''
    # Debugging output to check the first few nodes
    for node_id in list(graph.nodes)[:5]:
        if 'features' in graph.nodes[node_id]:
            print(f"Features for node {node_id}: {graph.nodes[node_id]['features']}")
        else:
            print(f"No features found for node {node_id}")
    '''

def extract_ego_node_id(filename):
    # The ego node ID is assumed to be the part before the first dot ('.') in the filename
    ego_node_id = filename.split('.')[0]
    return int(ego_node_id)  # Convert to integer if the ID is expected to be a numeric value

def load_egofeat(file_path, graph, ego_node_id):
    feature_names = graph.graph.get('feature_names', {})
    #print(f"Loading ego features from {file_path} for node {ego_node_id}")

    with open(file_path, 'r') as file:
        line = file.readline().strip()  # Assuming only one line for ego features
        features = list(map(int, line.split()))

        if ego_node_id not in graph:
            graph.add_node(ego_node_id)  # Ensure the ego node exists

        # Map feature indices to their descriptive names or default to 'feature_index'
        named_features = {feature_names.get(i, f'feature_{i}'): feat for i, feat in enumerate(features)}

        # For ego features, simply assign them as they are typically not merged with other features
        graph.nodes[ego_node_id]['features'] = named_features

        #print(f"Ego Features for node {ego_node_id}: {graph.nodes[ego_node_id]['features']}")



def load_featnames(file_path, graph):
    feature_names = {}
    with open(file_path, 'r') as file:
        for line in file:
            index, feature_description = line.strip().split(' ', 1)  # Assuming space is the delimiter
            feature_names[int(index)] = feature_description

    # Attach feature names to the graph as an attribute (useful for referencing later)
    graph.graph['feature_names'] = feature_names
    #print(f"Loaded feature names: {feature_names}")


def load_circles(file_path, graph):
    node_to_circles = {}  # Maps node to the list of circles it belongs to
    circle_to_nodes = {}  # Maps circle name to the set of nodes it includes
    
    #print(f"Loading circles from {file_path}")
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            circle_name = parts[0]  # The first part is the circle name
            circle_members = set(map(int, parts[1:]))  # The rest are node IDs
            
            # If circle is not present in circle_to_nodes, initialize it
            circle_to_nodes[circle_name] = circle_to_nodes.get(circle_name, set())
            
            # Add all members to the circle
            circle_to_nodes[circle_name].update(circle_members)
            
            for node_id in circle_members:
                # Add node to graph if not present
                if node_id not in graph:
                    graph.add_node(node_id)
                
                # Add circle to the node's list of circles
                node_to_circles.setdefault(node_id, set()).add(circle_name)
                
                # Update graph's node attribute
                graph.nodes[node_id]['circles'] = list(node_to_circles[node_id])
    
    return node_to_circles, circle_to_nodes


def build_network():
    # Initialize an empty Graph
    G = nx.Graph()
    # Path to the directory with all the data files
    base_path = 'facebook'

    # List all files in the directory
    files = os.listdir(base_path)
    for file in files:
        file_path = os.path.join(base_path, file)
        if file.endswith('.edges'):
            load_edges(file_path, G)
        elif file.endswith('.feat'):
            load_features(file_path, G)
        elif file.endswith('.egofeat'):
            ego_node_id = extract_ego_node_id(file)  # Extract the ego node ID from the filename
            load_egofeat(file_path, G, ego_node_id)  # Pass the extracted ID to the function
        elif file.endswith('.circles'):
            node_to_circles, circle_to_nodes= load_circles(file_path, G)
        elif file.endswith('.featnames'):
            load_featnames(file_path, G)


    print("Total number of nodes:", G.number_of_nodes())
    print("Total number of edges:", G.number_of_edges())
    return G





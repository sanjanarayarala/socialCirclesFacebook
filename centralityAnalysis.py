import networkx as nx
from nw_model.network import build_network

def centrality_analysis(graph, top_n=5):
    print("Centrality Analysis")
    
    #Calculating centralities
    degree = nx.degree_centrality(graph)
    betweenness = nx.betweenness_centrality(graph)
    closeness = nx.closeness_centrality(graph)
    try:
        eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000)
    except nx.PowerIterationFailedConvergence:
        print("Eigenvector centrality failed to converge, increasing max_iter.")
        eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=5000)  #Try larger number of iterations
    
    #Get top n nodes i.e. top 5 nodes, for each centrality measure
    top_degree = sorted(degree.items(), key=lambda item: item[1], reverse=True)[:top_n]
    top_betweenness = sorted(betweenness.items(), key=lambda item: item[1], reverse=True)[:top_n]
    top_closeness = sorted(closeness.items(), key=lambda item: item[1], reverse=True)[:top_n]
    top_eigenvector = sorted(eigenvector_centrality.items(), key=lambda item: item[1], reverse=True)[:top_n]
    
    print("Top nodes by Degree Centrality:")
    for node, cent in top_degree:
        print(f"Node {node}: {cent}")
    
    print("\nTop nodes by Betweenness Centrality:")
    for node, cent in top_betweenness:
        print(f"Node {node}: {cent}")
    
    print("\nTop nodes by Closeness Centrality:")
    for node, cent in top_closeness:
        print(f"Node {node}: {cent}")
    
    print("\nTop nodes by Eigenvector Centrality:")
    for node, cent in top_eigenvector:
        print(f"Node {node}: {cent}")


G=build_network() 
centrality_analysis(G)


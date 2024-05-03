import networkx as nx
from nw_model.network import build_network

def link_analysis(graph, top_n=5):
    print("Link Analysis")

    #calculate PageRank
    pagerank_scores = nx.pagerank(graph)

    #Calculate HITS scores
    hits_scores = nx.hits(graph, max_iter=100)  # max_iter may need to be adjusted based on convergence

    #Get top n, i.e. 5 nodes for PageRank and HITS measures
    top_pagerank = sorted(pagerank_scores.items(), key=lambda item: item[1], reverse=True)[:top_n]
    top_hubs = sorted(hits_scores[0].items(), key=lambda item: item[1], reverse=True)[:top_n]
    top_authorities = sorted(hits_scores[1].items(), key=lambda item: item[1], reverse=True)[:top_n]

    print("\nTop nodes by PageRank:")
    for node, score in top_pagerank:
        print(f"Node {node}: {score}")

    print("\nTop hub nodes by HITS:")
    for node, score in top_hubs:
        print(f"Node {node}: {score}")

    print("\nTop authority nodes by HITS:")
    for node, score in top_authorities:
        print(f"Node {node}: {score}")



G= build_network() 
link_analysis(G)

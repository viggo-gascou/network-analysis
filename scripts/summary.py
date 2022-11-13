# Imports 

import numpy as np 
import networkx as nx 
import matplotlib.pyplot as plt 
from collections import Counter
import seaborn as sns
from tabulate import tabulate

# -----------   GLOBAL MEASUREMENT FUNCTIONS  --------
def number_of_nodes(G):
    return nx.number_of_nodes(G)

def number_of_edges(G):
    return nx.number_of_edges(G)

def density(G):
    return nx.density(G)

def diameter(G):
    return nx.diameter(G)

def get_degrees(G):
    return [degree for _, degree in G.degree()]

def five_number_degree(degrees):
    return np.percentile(degrees, [0,25,50,75,100])

def degree_variance(degrees):
    return (np.sum([(degree - avg_degree(G))**2 for degree in degrees])) / len(degrees)

def global_clustering_coef(G):
    return nx.transitivity(G)

def avg_clustering_coef(G):
    return nx.average_clustering(G)

def avg_shortest_path(G):
    return nx.average_shortest_path_length(G)

# --------------- LOCAL MEASUREMNT FUNCTIONS --------------

def n_highest_closeness_centrality(G, n):
    dict_degree_closeness = dict(nx.closeness_centrality(G))
    # sort high to low
    sorted_list = sorted(dict_degree_closeness.items(), key = lambda x:x[1], reverse=True)[:n]
    li = [['--', n+1, sorted_list[n]] for n in range(len(sorted_list))]
    return li 

def n_highest_degree_centrality(G, n):
    # First make dict {node:degree_centrality}
    dict_degree_cent = dict(nx.degree_centrality(G))
    # sort high to low
    sorted_list = sorted(dict_degree_cent.items(), key = lambda x:x[1], reverse=True)[:n]

    li = [['--', n+1, sorted_list[n]] for n in range(len(sorted_list))]
    return li 

def n_highest_betweenness_centrality(G, n):
    # First make dict {node:degree_centrality}
    dict_degree_bc = dict(nx.betweenness_centrality(G))
    # sort high to low
    sorted_list = sorted(dict_degree_bc.items(), key = lambda x:x[1], reverse=True)[:n]
    li = [['--', n+1, sorted_list[n]] for n in range(len(sorted_list))]
    return li 

# -------- CLIQUES ------------

def maximal_cliques(G):
    #We take the largest compontent from the graph.  !!! No need to do this part if we choose to only look at the biggest connected component
    largest_cc = max(nx.connected_components(G), key=len)
    LG = G.subgraph(largest_cc)

    #Make a list with all cliques
    clique_list = list(nx.find_cliques_recursive(LG)) 

    #Use functions rom Networkx to find the largest clique and the number of maximal cliques in our graph
    largest_clique = nx.graph_clique_number(LG, clique_list) #Size of the largest of a clique
    maximal_cliques = nx.graph_number_of_cliques(LG, clique_list) #Return the number of max cliques

    print(f"Number of maximal cliques in the compontent: {maximal_cliques}")
    print(f"Largest clique in network: {largest_clique}.")


def final_return_statement(G, n):
    # G is an undirected, unweigthed graph
    # n is the number of nodes you want returned in the local measures

    # frame the data as a link of links in order to print tabulate
    degrees = get_degrees(G)
    five = five_number_degree(degrees)
    
    _global = [["Number of nodes: ", number_of_nodes(G)], ["Number of edges: ", number_of_edges(G)],["Diameter: ", diameter(G)], 
    ["Density of the graph: ", density(G)],["----------------","----------------"], ["Five number summary of the degrees: ", "----------------"], ["Minimum degree: ", five[0]],
    ["Lower Quantile: ", five[1]], ["Median Value: ", five[2]], ["Upper Quantile: ", five[3]], ["Maximum degree: ", five[4]],['Degree Variance:', degree_variance(degrees)],["----------------","----------------"],
     ["Global clustering coefficient: ", global_clustering_coef(G)], ["Average clustering coefficient: ", avg_clustering_coef(G)]
     , ["Average Shortest Path: ", avg_shortest_path(G)]]

    local = [['Closeness Centrality',' ' , ' ']] + n_highest_degree_centrality(G, n) + [['Betweenness Centrality', ' ', ' ']] + n_highest_betweenness_centrality(G,n) + [['Degree Centrality', ' ', ' ']] + n_highest_degree_centrality(G, n)
    

    print("                   GLOBAL MEASURES                  ")
    print("----------------------------------------------------")
    print(tabulate(_global, headers=["Measure", "Value"]))
    print("                   LOCAL MEASURES                  ")
    print("----------------------------------------------------")
    print(tabulate(local, headers=["Measure", "n", "Node, Measure"]))
    maximal_cliques(G)






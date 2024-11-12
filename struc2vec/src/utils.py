import numpy as np
import pandas as pd
import networkx as nx

def scale_weights(weights, min_scale=0.1, max_scale=10):
    """
    The functions takes a list of weights as input and rescales the values to 
    the set range min_scale-max_scale
    """
    min_weight = np.min(weights)
    max_weight = np.max(weights)
    scale = lambda x: (((max_scale-min_scale)*(x-min_weight))/(max_weight-min_weight))+min_scale
    return [scale(x) for x in weights]

def get_meta_data(G, nodes, embeddings, cmap=None):
    df_meta = pd.DataFrame([(node, embedding) for node,embedding in zip(nodes,embeddings)], columns=["Node", "Embedding"])

    # Clustering
    clustering = nx.clustering(G)
    df_meta["Clustering"] = [clustering[node] for node in df_meta["Node"]]

    # Betweenness centrality
    betweenness = nx.betweenness_centrality(G)
    df_meta["Betweenness_centrality"] = [betweenness[node] for node in df_meta["Node"]]

    # Closeness centrality
    closeness = nx.closeness_centrality(G)
    df_meta["Closeness_centrality"] = [closeness[node] for node in df_meta["Node"]]

    # In- and out-degree
    A = nx.adjacency_matrix(G, weight=None) # All cells are either 0 or 1 to support counting for degree
    ind2node = {i:node for i, node in enumerate(G.nodes())}
    # From the adj matrix, the in and out degree can be calculated as a sum of each row
    # and corresponding column
    degreeDict = {}
    for i in range(A.shape[0]):
        inDegree = A[:,[i]].sum()
        outDegree = A[[i],:].sum()
        degreeDict[ind2node[i]] = {"inDegree":inDegree, "outDegree":outDegree}
    df_meta["InDegree"] = [degreeDict[node]["inDegree"] for node in df_meta["Node"]]
    df_meta["OutDegree"] = [degreeDict[node]["outDegree"] for node in df_meta["Node"]]

    # Average weight (currently for bot in- and out-edges)
    avg_weight = {}
    for node in G.nodes():
        data = G[node]
        weights = []
        for dest, data in data.items():
            weights.append(data["weight"])
        avg_weight[node] = np.mean(weights)
    df_meta["Average_weight"] = [avg_weight[node] for node in df_meta["Node"]]

    # Groupby embeddings
    df_grouped = pd.DataFrame(df_meta.groupby("Embedding")["Node"].count())
    df_grouped.columns = ["Number of nodes"]

    if cmap:
        df_grouped["Color"] = [cmap[emb] for emb in df_grouped.index]
    
    avg_data = df_meta.drop("Node",axis=1).groupby("Embedding").mean().apply(lambda x: round(x, 3))

    return df_grouped.merge(avg_data, right_index=True, left_index=True)



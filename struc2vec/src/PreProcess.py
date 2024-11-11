import networkx as nx

def getDegreeSequences(G_UD, G_D):
    """
    The function takes an undirected and a directed network as input (from the same graph).

    It calculates the in- and out-degree sequences for each node for all layers of
    a the nodes neighborhoods

    The final output is a dictionary in the style {origin_node: {0:self, 1:degree_sequence 0 extended with 
    degree sequence from all immidiate neighbors, 2: degree_sequence 1 extended with degrees for 2-step neighbors}}
    """
    # 0
    A = nx.adjacency_matrix(G_D, weight=None) # All cells are either 0 or 1 to support counting for degree
    ind2node = {i:node for i, node in enumerate(G_D.nodes())}
    
    # 1
    # From the adj matrix, the in and out degree can be calculated as a sum of each row
    # and corresponding column
    degreeDict = {}
    for i in range(A.shape[0]):
        inDegree = A[:,[i]].sum()
        outDegree = A[[i],:].sum()
        degreeDict[ind2node[i]] = {"inDegree":inDegree, "outDegree":outDegree}

    # 2
    # For all node pairs the length of the shortest path are estimated, this will
    # then be used for generating the layers of neighborhoods by 'reversing' the dictionary
    all_shortest_paths = {node:paths for node, paths in nx.all_pairs_shortest_path_length(G_UD)}

    neighborhood_by_layer = {}
    for origin_node, neighbors in all_shortest_paths.items():
        neighborhood_by_layer[origin_node] = {}
        for node, layer in neighbors.items():
            if layer not in neighborhood_by_layer[origin_node]:
                neighborhood_by_layer[origin_node][layer] = []
            neighborhood_by_layer[origin_node][layer].append(node)

    # 3
    # Now each vector of nodes generated in #2 are converted to their corresponding in-
    # and out-degree which was calculated in #1.
    # Each degree sequence is aggregated from the current layer and all previous layers.
    degree_vectors = {}

    for origin_node, neighborhoods in neighborhood_by_layer.items():
        degree_vectors[origin_node] = {}
        for layer, nodes in neighborhoods.items():
            vector_in = [degreeDict[node]["inDegree"] for node in nodes]
            vector_out = [degreeDict[node]["outDegree"] for node in nodes]
            if layer == 1:
                degree_vectors[origin_node][layer] = {"in": vector_in, "out":vector_out}
            else:
                vec_in_prev = degree_vectors[origin_node][layer-1]["in"].copy()
                vec_in_prev.extend(vector_in)

                vec_out_prev = degree_vectors[origin_node][layer-1]["out"].copy()
                vec_out_prev.extend(vector_out)

                degree_vectors[origin_node][layer] = {}
                degree_vectors[origin_node][layer]["in"] = vec_in_prev
                degree_vectors[origin_node][layer]["out"] = vec_out_prev

    # 4
    # Finally return the dictionary
    return degree_vectors


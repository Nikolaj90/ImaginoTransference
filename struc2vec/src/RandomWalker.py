import numpy as np


def random_walk_step(current_node, s2vG, n_layer):
    '''
    The function picks a random node from the current nodes neighbors based on probabilities calculated from adjacency dict
    '''
    adj_dict = s2vG.adj_dicts[n_layer]
    weight_total = sum(adj_dict[current_node].values())
    neigh = list(adj_dict[current_node].keys())
    prob = [w / weight_total for w in adj_dict[current_node].values()]
    return np.random.choice(neigh, size=1, p=prob)[0]

def random_walk(s2vG, start_node, number_of_walks, walk_length, q):
    # Start at the bottom layer
    n_layer = 0
    walks = []
    for i in range(number_of_walks):
        current_node = start_node if start_node else np.random.choice(s2vG.nodes)
        walk = [current_node]
        for j in range(walk_length):
            n_layer = getLayer(s2vG, n_layer, current_node, q)
            current_node = random_walk_step(current_node, s2vG, n_layer)
            walk.append(current_node)
        walks.append(walk)
    return walks

def getLayer(s2vG, n_layer, current_node, q):
    if np.random.random() > q:
        return n_layer
    else:
        up_p = s2vG.upweightdict[n_layer][current_node]
        if n_layer == 0:
            n_layer = 1
        elif n_layer == s2vG.n_layers:
            n_layer = n_layer - 1
        elif (np.random.random() >= up_p):
            n_layer = n_layer - 1
        else:
            n_layer = n_layer + 1
        return n_layer

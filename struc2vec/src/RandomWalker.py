import numpy as np

class RandomWalker():
    def __init__(self):
        pass
    
    def random_walk_step(self, current_node, s2vG, n_layer):
        '''
        The function picks a random node from the current nodes neighbors based on probabilities calculated from adjacency dict
        '''
        adj_dict = s2vG.adj_dicts[n_layer]
        weight_total = sum(adj_dict[current_node].values())
        neigh = list(adj_dict[current_node].keys())
        prob = [w / weight_total for w in adj_dict[current_node].values()]
        return np.random.choice(neigh, size=1, p=prob)[0]
    
    def random_walk(self, s2vG, start_node, number_of_walks, walk_length, q):
        # Start at the bottom layer
        n_layer = 0
        walks = []
        layers = []
        for i in range(number_of_walks):
            if start_node:
                current_node = start_node
            else:
                current_node = np.random.choice(s2vG.nodes)
            walk = []
            layer = []
            walk.append(current_node)
            layer.append(n_layer)
            for j in range(walk_length):
                n_layer = self.getLayer(s2vG, n_layer, current_node, q)
                current_node = self.random_walk_step(current_node, s2vG, n_layer)
                walk.append(current_node)
                layer.append(n_layer)
            walks.append(walk)
            layers.append(layer)
        return walks, layers

    def getLayer(self, s2vG, n_layer, current_node, q):
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

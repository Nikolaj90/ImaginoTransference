import src.GraphAlgorithms as ga
import src.RandomWalker as rw

class struc2vec():
    def __init__(self, G):
        '''
        First a graph object is created, this stores the relevant information of the graph and allows the application
        of the struc2vec algorithm and storing the results.
        '''
        self.G = G
        self.nodes = [*G.nodes] # List of all nodes
        self.nodePairs = self.getNodePairs()
    
    def getNodePairs(self):
        # Get all unique node pairs as tuples ignoring order
        nodePairs = []
        for i, v in enumerate(self.nodes[:-1]):
            for d in self.nodes[i+1:]:
                nodePairs.append((v,d))
        return nodePairs
    
    def getMultiLevelGraph(self, n_level):
        self.G_ML, self.adj_dicts = ga.MultiLevelGraph(self, n_level)
        self.n_layers = n_level
        self.upweightdict = ga.getUpWeightDict(self.G_ML)

    def getRandomWalks(self, start_node=None, number_of_walks=100, walk_length=10, q=0.2):
        return rw.random_walk(self, start_node, number_of_walks, walk_length, q)
        

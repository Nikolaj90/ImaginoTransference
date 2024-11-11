from struc2vec.GraphAlgorithms import GraphAlgorithms as ga
from struc2vec.RandomWalker import RandomWalker as rw
import networkx as nx

class struc2vec():
    def __init__(self, G):
        '''
        First a graph object is created, this stores the relevant information of the graph and allows the application
        of the struc2vec algorithm and storing the results.
        '''
        self.G = G
        self.nodes = [*G.nodes] # List of all nodes
        self.nodePairs = self.getNodePairs()
        self.diameter = nx.diameter(G)
    
    def getNodePairs(self):
        # Get all unique node pairs as tuples ignoring order
        nodePairs = []
        for i, v in enumerate(self.nodes[:-1]):
            for d in self.nodes[i+1:]:
                nodePairs.append((v,d))
        return nodePairs
    
    def getMultiLevelGraph(self, path=None):
        """
        This function generates and saves the context graph for the random walks. It has no output, but saves the G_ML for the object.

        If the context graph has been created, it takes the path as input, and loads and stores the G_ML in the object instead.
        """
        if path:
            if path[-1] != "/":
                path = path + "/"
        self.G_ML, self.adj_dicts = ga().MultiLevelGraph(self,self.diameter,path=path)
        self.n_layers = self.diameter
        self.upweightdict = ga().getUpWeightDict(self.G_ML)

    def getRandomWalks(self, start_node=None, number_of_walks=100, walk_length=10, q=0.2):
        walks = rw().random_walk(self,start_node, number_of_walks, walk_length, q)
        return walks
        

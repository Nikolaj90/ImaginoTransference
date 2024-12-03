import numpy as np
import fastdtw
import networkx as nx
import os

class GraphAlgorithms():
    def __init__(self):
        '''
        This object contains the different functions to be applied on the graph object for the struc2vec algorithm.
        '''
        pass
    
    # def getDegreeSequence(self, s2vG, origin, n_steps):
    #     '''
    #     The function returns a sorted degree sequence for a given node based on 
    #     n-step neighbors.
    #     '''
    #     visitedNodes = {}
    #     que = [origin]
    #     for _ in range(n_steps):
    #         newQue = []
    #         for node_0 in que:
    #             if node_0 not in visitedNodes:
    #                 visitedNodes[node_0] = len(s2vG.G[node_0])
    #             for node_1 in s2vG.G[node_0]:
    #                 if node_1 not in visitedNodes:
    #                     newQue.append(node_1)
    #         que = newQue
    #     degreeSequence = sorted(visitedNodes.values(), reverse=True)
    #     return degreeSequence
    
    # def getDSlayer(self, s2vG, n_steps):
    #     '''
    #     For a given layer, get the degree sequence for all nodes
    #     '''
    #     nodeDS = {} # Container for Degree sequences
    #     for v in s2vG.nodes:
    #         # Calculate degree sequence and store it indexed by node
    #         DS = self.getDegreeSequence(s2vG, v, n_steps)
    #         nodeDS[v] = DS
    #     return nodeDS
    
    # def calcDTW(self, s2vG, n_steps):
    #     '''
    #     Calculate DTW distance between DS for each node in nodepairs and return the distance between all nodepairs
    #     '''
    #     # For the calculation, we first need to get the degree sequence for each node
    #     nodeDS = self.getDSlayer(s2vG, n_steps)
        
    #     ssm_nodepairs = {}
    #     for v0, v1 in s2vG.nodePairs:
    #         # Each DS is converted to an numpy array and reshaped into 1-D arrays (or rather (n,1) 
    #         # where n is the length of the array)
    #         ds0 = np.array(nodeDS[v0])
    #         ds0 = ds0.reshape(len(ds0),1) 
    #         ds1 = np.array(nodeDS[v1])
    #         ds1 = ds1.reshape(len(ds1),1)

    #         distance, path = fastdtw.fastdtw(ds0, ds1, dist=self.d_func)
    #         ssm_nodepairs[(v0,v1)] = distance
    #     return ssm_nodepairs

    def d_func(self,a,b):
        '''
        Calculate distance
        '''
        return float((max(a,b)/min(a,b))-1)
    
    def calculateDistances(self, s2vG, n_steps):
        """
        The function utilizes the preprocessed degreesequences and calculates a distance
        measure for the in- and out-degree sequences between all node pairs.

        The final distance measure is the average of the in- and out-distances.

        The output is a dictionary with a tuple of the nodepairs as key and distance as value
        """
        edgelist_dist = []
        for v0, v1 in s2vG.nodePairs:
            arr0_in = np.array(sorted(s2vG.DegreeSequences[v0][n_steps]["in"], reverse=True))
            arr0_out = np.array(sorted(s2vG.DegreeSequences[v0][n_steps]["out"], reverse=True))
            arr1_in = np.array(sorted(s2vG.DegreeSequences[v1][n_steps]["in"], reverse=True))
            arr1_out = np.array(sorted(s2vG.DegreeSequences[v1][n_steps]["out"], reverse=True))

            arr0_in = arr0_in.reshape(len(arr0_in),1)
            arr1_in = arr1_in.reshape(len(arr1_in),1)
            arr0_out = arr0_out.reshape(len(arr0_out),1)
            arr1_out = arr1_out.reshape(len(arr1_out),1)

            arr0_in = arr0_in + np.ones((len(arr0_in),1))
            arr1_in = arr1_in + np.ones((len(arr1_in),1))
            arr0_out = arr0_out + np.ones((len(arr0_out),1))
            arr1_out = arr1_out + np.ones((len(arr1_out),1))

            dist_in, conv_vect = fastdtw.fastdtw(arr0_in, arr1_in, dist=self.d_func)
            dist_out, conv_vect = fastdtw.fastdtw(arr0_out, arr1_out, dist=self.d_func)

            prev_weight = 0
            if n_steps != 0:
                prev_weight = self.G_ML[n_steps-1].edges[v0,v1]["weight"]
            edge = (v0,v1,{"weight": prev_weight + np.exp(-np.mean([dist_in, dist_out]))})
            edgelist_dist.append(edge)
        return edgelist_dist

    # def getStrucGraph(self, s2vG, n_steps):
    #     '''
    #     This function will calculate the context graph for a specified layer in graph generated from structural similarity.

    #     It takes s2vG-object as input and the number of layers of neighbors to include for comparison of each node pair.
    #     '''
    #     G = nx.Graph()
        
    #     # To generate the graph we need to calculate the similarity scores for all nodepairs
    #     # To do this, we will calculate the DTW distance based on similarity measures of each node
    #     dist_nodepairs = self.calculateDistances(s2vG, n_steps)
        
    #     # Now all the edges are added and the weight is calculated
    #     for (v0,v1), dist in dist_nodepairs.items():
    #         G.add_edge(v0,v1,weight=dist)
    #     return G
    
    def MultiLevelGraph(self, s2vG, n_level, path=None):
        """
        This function takes a s2vG-object as input and generates the responding context graph for it. If a path is defined, it loads the graph otherwise the graph is 
        created. It outputs the context graph as a dictionary object, with layers as keys and graphs as values.
        """
        self.G_ML = {}
        if path:
            for file in os.listdir(path):
                layer_n = int(file.split(".")[0])
                graph = nx.read_gexf(path + file)
                self.G_ML[layer_n] = graph
        else:
            for i in range(n_level+1):
                edgelist_i = self.calculateDistances(s2vG, i)
                G_i = nx.Graph(edgelist_i)
                self.G_ML[i] = G_i

        adj_dicts = self.getAdjacencyDicts(self.G_ML)
        return self.G_ML, adj_dicts

    
    def getAdjacencyDicts(self, G_ML):
        adj_dicts = {}
        for layer, graph in G_ML.items():
            adj_dicts[layer] = {}
            for node, neighbors in graph.adjacency():
                adj_dicts[layer][node] = {neighbor:attr["weight"] for neighbor, attr in neighbors.items()}
        return adj_dicts
    
    def getUpWeightsLayer(self, G):
        '''
        The function takes a graph as input, and calculates the edge weight for all node-node edges from layer n 
        to layer n+1.
        It returns a dictionary with nodes as keys and weight as value.
        '''
        # Calculate mean weight of all edges in graph
        avg_edge_weight = np.mean([G.edges[edge]["weight"] for edge in G.edges])

        # Dict for edges
        upEdge = {}

        # Get weight for each node
        for node in G.nodes:
            aboveAvgEdgeWeight = np.mean([int(att["weight"] >= avg_edge_weight) for edge, att in G[node].items()])
            upWeight = np.log(aboveAvgEdgeWeight + np.exp(1))
            upEdge[node] = upWeight / (upWeight+1)

        return upEdge


    def getUpWeightDict(self, G_multilayer):
        '''
        The function takes a dictionary for a multilayer graph as input, and returns a 
        dictionary of all node-node edge weights for each layer in the multilayer graph.
        The function is an iterator, utilizing the function getUpWeightsLayer to retrieve weights for each layer
        '''
        upWeightDict = {}
        for layer, G in G_multilayer.items():
            upWeightsLayer = self.getUpWeightsLayer(G)
            upWeightDict[layer] = upWeightsLayer
        return upWeightDict
    
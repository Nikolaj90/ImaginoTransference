import numpy as np
import fastdtw
import networkx as nx



def getDegreeSequence(s2vG, origin, n_steps):
    '''
    The function returns a sorted degree sequence for a given node based on 
    n-step neighbors.
    '''
    visitedNodes = {}
    que = [origin]
    for _ in range(n_steps):
        newQue = []
        for node_0 in que:
            if node_0 not in visitedNodes:
                visitedNodes[node_0] = len(s2vG.G[node_0])
            for node_1 in s2vG.G[node_0]:
                if node_1 not in visitedNodes:
                    newQue.append(node_1)
        que = newQue
    degreeSequence = sorted(visitedNodes.values(), reverse=True)
    return degreeSequence

def getDSlayer(s2vG, n_steps):
    '''
    For a given layer, get the degree sequence for all nodes
    '''
    nodeDS = {v: getDegreeSequence(s2vG, v, n_steps) for v in s2vG.nodes } # Container for Degree sequences
    return nodeDS

def d_func(a,b):
    '''
    Calculate distance
    '''
    return float((max(a,b)/min(a,b))-1)

def calcDTW(s2vG, n_steps):
    '''
    Calculate DTW distance between DS for each node in nodepairs and return the distance between all nodepairs
    '''
    # For the calculation, we first need to get the degree sequence for each node
    nodeDS = getDSlayer(s2vG, n_steps)
    
    ssm_nodepairs = {}
    for v0, v1 in s2vG.nodePairs:
        # Each DS is converted to an numpy array and reshaped into 1-D arrays (or rather (n,1) 
        # where n is the length of the array)
        ds0 = np.array(nodeDS[v0])
        ds0 = ds0.reshape(len(ds0),1) 
        ds1 = np.array(nodeDS[v1])
        ds1 = ds1.reshape(len(ds1),1)

        distance, path = fastdtw.fastdtw(ds0, ds1, dist=d_func)
        ssm_nodepairs[(v0,v1)] = distance
    return ssm_nodepairs

def getStrucGraph(s2vG, n_steps):
    '''
    This function will calculate the graph for a specified layer in graph generated from structural similarity
    '''
    G = nx.Graph()
    
    # To generate the graph we need to calculate the similarity scores for all nodepairs
    # To do this, we will calculate the DTW distance based on similarity measures of each node
    ssm_nodepairs = calcDTW(s2vG, n_steps)
    
    # Now all the edges are added and the weight is calculated
    for (v0,v1), ssm in ssm_nodepairs.items():
        G.add_edge(v0, v1, weight= np.exp(-ssm))
    return G

def MultiLevelGraph(s2vG, n_level):
    G_ML = {i:getStrucGraph(s2vG, i) for i in range(n_level+1)}
    adj_dicts = getAdjacencyDicts(G_ML)
    return G_ML, adj_dicts


def getAdjacencyDicts(G_ML):
    adj_dicts = {}
    for layer, graph in G_ML.items():
        adj_dicts[layer] = {}
        for node, neighbors in graph.adjacency():
            adj_dicts[layer][node] = {neighbor:attr["weight"] for neighbor, attr in neighbors.items()}
    return adj_dicts

def getUpWeightsLayer(G):
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


def getUpWeightDict(G_multilayer):
    '''
    The function takes a dictionary for a multilayer graph as input, and returns a 
    dictionary of all node-node edge weights for each layer in the multilayer graph.
    The function is an iterator, utilizing the function getUpWeightsLayer to retrieve weights for each layer
    '''
    upWeightDict = {}
    for layer, G in G_multilayer.items():
        upWeightsLayer = getUpWeightsLayer(G)
        upWeightDict[layer] = upWeightsLayer
    return upWeightDict

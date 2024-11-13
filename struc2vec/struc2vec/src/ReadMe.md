# struc2vec - a replication
A replication of the _struc2vec_ algortihm as designed by _Ribeiro, Saverse and Figueiredo (2017)_.

## Quick tutorial
Import libraries and module
```python
import src.struc2vec  as s2v
import networkx as nx
from gensim.models import Word2Vec
import numpy as np
from sklearn.decomposition import PCA
```
I will construct a barbell graph, given that it is great for initial evaluation of performance. After consting the graph, I will construct a graph object with the s2v module.

```python
G = nx.barbell_graph(20, 5)

s2vG = s2v.struc2vec(G)
```

### Constructing the context graph
I create the multilevel graph and define the number of layers in the graph. The graph is created as a dict-object in with the syntax {layer_0:graphObject_0, ..., layer_n: graphObject_n} and can be accessed as s2vG.G_ML.

```python
s2vG.getMultiLevelGraph(3)
```

### Generating context for nodes
Then I use get a number of random walks, this can be done by providing a starting point (as I do in this example, getting random walks for all nodes), if no starting node is provided a random node is chosen for each walk.

```python
walks = []
for node in s2vG.nodes:
    walk_node, layers = s2vG.getRandomWalks(start_node = node, number_of_walks = 300, walk_length=15)
    walks.extend(walk_node)
```

### Learning a language model
Finally I use the Word2vec algorithm and PCA, to create the embeddings and categorise the nodes.

```python
model = Word2Vec(walks, vector_size=50)

embeddings = {node: model.wv[node] for node in s2vG.nodes}

X = np.array(list(embeddings.values()))

pca = PCA(n_components=3)
X_transform = pca.fit_transform(X)

node_embeddings = {}
for node, embedding in enumerate(X_transform):
    emb_list = list(embedding)
    index = emb_list.index(max(emb_list))
    node_embeddings[node] = index
```


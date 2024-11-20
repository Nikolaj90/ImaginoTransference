# Process from analysis to report
For my own sanity, I will make a step-by-step guide for the process of making a structural network analysis and testing it. So that I know where all of the steps are done, and where the outputs are stored.

## 0. Initial definitions
Migration is measured as the difference in migrant stock between one year and another for every destination country - for this analysis that difference is measured between 2017 and 2015. All negative differences are set to 0.
The destination country is the migrants current residence at the time of each population count.
The origin country is defined as the birth place of the migrant.

For all meta data about countries, it is the data measured for the year 2015 that will be used in the analysis.

## 1. Data preparation
I have preprocessed some data from the UN migration database, and population data for each country. This is loaded and an edgelist is created with origin, destination and weight - weight refers to the number of migrants from the origin country, that has migrated to the destination country, it is re-scaled, such that it is the number of migrants per 10000 people out of the origin countries population.

I then create four graphs, where I remove nodes based on the average weight of the stochastic matrix. I then have a graph with 25%, 50% and 75% and one with all edges. \
_Currently placed in the analysis and I might also want to remove edges based on the specific node rather than on the average. Seems more intuitive_ 

## 2. struc2vec setup
I run the initial setup via my struc2vec algorithm, creating context graphs for all four graphs.

## 3. Hyperparameter testing
Before calculating the embeddings, I have tested some of the hyperparameters and their relation to the outcome. There is no perfect way of making this decision - this is a very big issue with this method, given that it takes a lot of calculations to even test how much the different embedding will vary from one another. 

My final choices has been on hyperparameters, that from a qualitative analysis seems to _converge_ on some average statistics across the different measurements. This is far from an ideal way of chosing hyperparameters, and more work needs to be put in to making this part of the analysis.

## 4. Creating context and embeddings
Now I do random walks on each of the four graphs, with twice as many walks on the graphs with 75% and 50% of the edges. This is a choice I have made, because the edges with smallest weights carries the least amount of information about the migration of a country, but the most amount of information about the pattern of each node. Oppositionally the the graph with only edges with the highest weight carries the most amount of information on the migration of a country, but the least information about the migration pattern of each node. The two middle graphs I argue are most accurate in providing information on both actual migration and pattern.

All of the walks are used for context to create the embeddings with word2vec.

From the embedding I make a scree plot to determine the number of components for my PCA.

## 5. Testing the results
I am interested in learning about my classifications; both from a network perspective and from the perspective of development features. Each is tested separatly and meta data is found on the node/country-level.

When testing these, I make a dummy variable of the classes excluding one as reference (currently this is the classification with the lowest human development index average). For each feature to be tested, I make a linear regression with the target variable being the feature and the independent variable are the classifications. This is to make an estimate of the level of variance within group and how distinct each group are. 

It also descripes some features of each classifications.

### 5.1 Structural network features of nodes
I measure several structural features of each node - centrality, clustering, degree, average weight, and similar. It is expected that there will be some correlation by design, but this indicates how the structural features relates to each classification and how strongly.

### 5.2 Development features for countries
From the UN development program, several development scores are published for countries. I have chosen a subset of these and related them to the countries in my analysis. I have also added GDP, fertility rate and mortality rate, because these are related to development according to literature - although they are not themselves indicative of development.

### 5.3 Tables!
Finally, from the parameters of the two linear regressions and the p-value of each, I create two tables for the report. Each is separate and then compared to make an argument for whether structural features and development seems to be correlated and able to measure with this procedure.

## 6. Visualisations
For the report I will also need some visualisations of my results. These are not necessarily all included but potential visualisations.

#### World map, with and/or without network
I have made a world map of all countries and colored each country according to their classification. 

I also have the choice to overlay the network with the centroid as nodes. This is unfortunately quite difficult to read.

#### Alluvial diagram / Sankey diagram
Flow from origin to destination countries divided into classifications.
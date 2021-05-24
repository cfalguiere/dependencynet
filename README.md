# dependencynet
Dependency representation and analysis with graphs (networks)




# Changelog

## 0.2.0-SNAASHOT
Refactoring of core classes
Tests refactoring
Added full scenarios
Lint and smoke test of notebooks

## 0.1.9
Fix bug #8 GraphMl generation fail when nodes already exists

## 0.1.8
Fix bug #2 PyYed generation failed if graph use connections

## 0.1.7
Fix bug #3 Missing links while using resources connections
- now support links from one node to many nodes

## 0.1.6
minor fixes

## 0.1.5
New features:
- allow to make a copy of a network in order to alter the copy
- allow to add input/output role to resources and connect output to input
- allow to remove nodes having a given category
- allow to aggregate the levels
- allow to replace input/output connection with a single node
- allow to fold categories and show links through
- get a summary of the graph content

Some refactoring:
- package datasource.loaders is now datasource.core
- minor change of schema interface for input/output connections

## 0.1.3 - 0.1.4
Bug fixes:
- packaging issue (missing dependencies)

## 0.1.2
New features:
- allow to type resource as input / output
- inputs are directed toward the node

## 0.1.1
New features:
- helper to build the cytoscape style document
- helper convert the graph into a pyyed file (GraphML)

## 0.1.0
New features:
- Build a networkx/cytoscape network

Improvements of Data Loader:
- explode a list a column consisting in a items into multiple lines
- ignore nan in resource columns

## 0.0.5
New features:
- Load a 3 levels hierarchy and resources

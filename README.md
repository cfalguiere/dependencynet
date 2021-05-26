# dependencynet

This module wraps some data and graph manipulation tools to help analyzing and building representations of directed graphs.

This modules make it easier to build graph with the properties listed below
- elements can be categorized as levels and resources
- levels consists of composite keys forming a hierarchy, for instance
    - area > country > town
    - group > artifact > version
    - package > class > function
    - owner > table > attribute
    - workflow > step > task
- resource is any element related to a level (and only one), for instance
    - monuments or POI of a town
    - tables used by a class
- resources having the same label might be connected to each other to form new dependencies, for instance
    - files in and out of a workflow task  might be connected to each other to form data flows
    - towns may be connected to form a trip if one has a flight out and the other a flight in with both having the same label

What can I do with this tool ?
- analyse of dependencies in code bases
- analyse of data flows between tasks or microservices

## Stems of this projects

This project stems from the need of featuring out how a large very messy project is made. I started by trying to list and connect elements manually, then I automated some parts. I ended up with a lot of very messy scripts to extract the most visible dependencies and it helped me to draw some schemas in Powerpoint.

That pointed me to the fact that this system was a graph, a network of workflows, treatments, tasks, classes, tables, exported files, external packages, delivery bundles. I could clean up a little bit by representing all these elements as a graph and when this step is done it is easier to select what kind of nodes and links I want to show for a given task. Graph tools may also help to produce schemas.

I started to rework those scripts in Python notebooks as a side project. It took me a while. Graphs are powerful, but power comes with lots of concepts to master. In the Python ecosystem, networkx is the library to go with graphs. It has a lot of graph manipulation features but charts are not so easy, and charts was the main goal. I found ipycytoscape (a port of cytoscape) easy to use with charts. But I lacked some networkx features. Hopefully there are ways to integrate networkx and cytoscape. I also had a lot of pandas code to collect and build data structues required by the graph libraries. Again, I had a lot of code to maintain in order to achieve my goals.

The last rework is this library. I factored out functions I found useful in the process of building the analyze tool. This is also a way to learn how to make a module library in Python. I try do make it as clean as possible.

Please keep in mind that
- this is a side project
- it is not intended to cover all the needs but a provide a specific subset required to easily build, clean up and show directed graphs of connected elements


## concepts
The graph production is done in 4 major steps

- Model : build datasource for each type of elements and organize levels hierarchy
    - Schema : describe the Model metadata (levels, resources, connections)
- GraphModel : represents the Model as a networkx graph
- GraphViewer : encapsulate the steps to show the cytoscape graph
    - StyleBuilder : generates a convenient cytoscape style from the schema
- GraphMLConverter : turns the graph and the style into a GraplML file for Yed

TODO link to Yed

## How to install

To use this library please use
```
pip install dependencynet
```

If you want to build from the sources, please clone the repository and run setup

## Main libraries
This project rely on the following libraries
- pandas
- networks
- ipycytoscape
- pyyed
- nox
- flake8
- pytest

TODO links and description from the module

Thanks to the maintainers and contributors of these modules.

## Changelog

### 0.2.0-SNAPSHOT
Refactoring of core classes
Tests refactoring
Added full scenarios
Lint and smoke test of notebooks

### 0.1.9
Fix bug #8 GraphMl generation fail when nodes already exists

### 0.1.8
Fix bug #2 PyYed generation failed if graph use connections

### 0.1.7
Fix bug #3 Missing links while using resources connections
- now support links from one node to many nodes

### 0.1.6
minor fixes

### 0.1.5
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

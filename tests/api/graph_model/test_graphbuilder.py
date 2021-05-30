"""
This module tests the graph builder
"""
# third party import
import pytest

from os import path
import pandas as pd

from dependencynet.model import ModelBuilder

# module import
from dependencynet.network.graphbuilder import GraphBuilder, LevelNode, ResourceNode


@pytest.fixture
def source_data_towns(schema_towns, compact_columns_towns):
    filename = path.join('tests', 'resources', 'data', 'compact', 'towns.csv')
    data = pd.read_csv(filename, delimiter=';')

    df = pd.DataFrame(data, columns=compact_columns_towns)
    return df


@pytest.fixture
def model_towns(source_data_towns, schema_towns):
    model = ModelBuilder().from_compact(source_data_towns) \
                          .with_schema(schema_towns) \
                          .render()
    return model


class AreaNode(LevelNode):
    def __init__(self, properties):
        super().__init__(properties, 'area')


class CountryNode(LevelNode):
    def __init__(self, properties):
        super().__init__(properties, 'country')


class TownNode(LevelNode):
    def __init__(self, properties):
        super().__init__(properties, 'town')


class MonumentNode(ResourceNode):
    def __init__(self, properties):
        super().__init__(properties, 'monument')


@pytest.fixture
def class_mapping_towns():
    return {'area': AreaNode, 'country': CountryNode, 'town': TownNode, 'monument': MonumentNode}


# Tests
def test_graph_builder_towns(class_mapping_towns, model_towns):
    graph_model = GraphBuilder().with_types(class_mapping_towns).with_model(model_towns).render()
    assert graph_model

    nodes = list(graph_model.G.nodes(data=True))
    assert nodes

    nodeA01 = nodes[0][0]
    assert nodeA01.classes == 'area level'
    assert nodeA01.data['id'] == 'A01'
    assert nodeA01.data['label'] == 'A01 Europe'
    assert nodeA01.data['category'] == 'area'
    assert nodeA01.data['group'] == 'level'

    nodeA01C01 = nodes[2][0]
    assert nodeA01C01.classes == 'country level'
    assert nodeA01C01.data['id'] == 'A01C01'
    assert nodeA01C01.data['label'] == 'A01C01 France'
    assert nodeA01C01.data['category'] == 'country'
    assert nodeA01C01.data['group'] == 'level'

    nodeA01C01T01 = nodes[6][0]
    assert nodeA01C01T01.classes == 'town level'
    assert nodeA01C01T01.data['id'] == 'A01C01T01'
    assert nodeA01C01T01.data['label'] == 'A01C01T01 Paris'
    assert nodeA01C01T01.data['category'] == 'town'
    assert nodeA01C01T01.data['group'] == 'level'

    nodeA01C01T01M01 = nodes[11][0]
    assert nodeA01C01T01M01.classes == 'monument resource'
    assert nodeA01C01T01M01.data['id'] == 'A01C01T01M01'
    assert nodeA01C01T01M01.data['label'] == 'A01C01T01M01 Eiffel Tower'
    assert nodeA01C01T01M01.data['category'] == 'monument'
    assert nodeA01C01T01M01.data['group'] == 'resource'

    edges = list(graph_model.G.edges)
    assert edges

    edge1 = edges[0]
    assert edge1[0].data['id'] == 'A01'
    assert edge1[1].data['id'] == 'A01C01'

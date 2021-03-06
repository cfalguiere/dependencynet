"""
This module tests the graph model
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
def test_remove_category(class_mapping_towns, model_towns):
    graph_model = GraphBuilder().with_types(class_mapping_towns).with_model(model_towns).render()
    assert graph_model

    graph_model.remove_category('area')

    nodes = list(graph_model.G.nodes(data=True))
    assert nodes

    nodeA01C01 = nodes[0][0]
    assert nodeA01C01.classes == 'country level'
    assert nodeA01C01.data['id'] == 'A01C01'

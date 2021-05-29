"""
Fixtures for towns twolevels
purpose : two levels and one resource
The dataset has
- 2 levels : Country, Town
- 1 resource: monument
- explode list of monument in column monument
"""
import pytest
from os import path

import pandas as pd

# module import
from dependencynet.schema import SchemaBuilder
from dependencynet.model import ModelBuilder

from dependencynet.network.graphbuilder import LevelNode, ResourceNode


@pytest.fixture
def schema_towns():
    schema = SchemaBuilder().level('country', 'C') \
                            .level('town', 'T') \
                            .resource('monument', 'M', explode=True, delimiter=',') \
                            .render()
    return schema


@pytest.fixture(scope="session")
def compact_columns_towns():
    columns = ['country', 'town', 'monument']
    return columns


@pytest.fixture
def source_data_towns(schema_towns, compact_columns_towns):
    filename = path.join('tests', 'scenario', 'twolevels', 'resources', 'towns-2levels.csv')
    data = pd.read_csv(filename, delimiter=';')

    df = pd.DataFrame(data, columns=compact_columns_towns)

    # FIXME factprize
    return df


@pytest.fixture
def model_towns(source_data_towns, schema_towns):
    model = ModelBuilder().from_compact(source_data_towns) \
                          .with_schema(schema_towns) \
                          .render()

    return model


@pytest.fixture
def class_mapping_towns():
    return {'country': CountryNode, 'town': TownNode,
            'monument': MonumentNode}


# networkx classes

class CountryNode(LevelNode):
    def __init__(self, properties):
        super().__init__(properties, 'country')


class TownNode(LevelNode):
    def __init__(self, properties):
        super().__init__(properties, 'town')


class MonumentNode(ResourceNode):
    def __init__(self, properties):
        super().__init__(properties, 'monument')

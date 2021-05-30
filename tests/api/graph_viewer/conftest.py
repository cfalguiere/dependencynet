"""
test fixtures
"""

# third party import
import pytest

import logging
from os import path
import pandas as pd

from dependencynet.schema import SchemaBuilder
from dependencynet.network.graphbuilder import GraphBuilder
from dependencynet.network.graphbuilder import LevelNode, ResourceNode, InputNode, OutputNode
from dependencynet.model import ModelBuilder
from dependencynet.network.stylebuilder import StyleBuilder


@pytest.fixture(autouse=True, scope="session")
def logger():
    logging.basicConfig()
    logger = logging.getLogger('test_datasets_utils')
    logger.setLevel(logging.DEBUG)


# ### Towns

# (scope="session")
@pytest.fixture
def schema_towns():
    schema = SchemaBuilder().level('area', 'A') \
                            .level('country', 'C') \
                            .level('town', 'T') \
                            .resource('monument', 'M', explode=True, delimiter=',') \
                            .render()
    return schema


@pytest.fixture
def compact_columns_towns():
    columns = ['area', 'country', 'town', 'monument']
    return columns


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


@pytest.fixture
def graph_model_towns(class_mapping_towns, model_towns):
    graph_model = GraphBuilder().with_types(class_mapping_towns).with_model(model_towns).render()
    return graph_model


@pytest.fixture
def graph_style_towns(schema_towns):
    graph_style = StyleBuilder(schema_towns).render()
    return graph_style


# Trips


@pytest.fixture
def schema_trips():
    schema = SchemaBuilder().level('area', 'A').level('country', 'C').level('town', 'T') \
                              .resource('flight_in', 'FIn', role='INPUT', connect_id_name='flight') \
                              .resource('flight_out', 'FOut', role='OUTPUT', connect_id_name='flight') \
                              .connect('flight_out', 'flight_in') \
                              .render()
    return schema


@pytest.fixture(scope="session")
def compact_columns_trips():
    columns = ['area', 'country', 'town', 'flight_in', 'flight_out']
    return columns


@pytest.fixture
def source_data_trips(schema_trips, compact_columns_trips):
    filename = path.join('tests', 'resources', 'data', 'compact', 'trips.csv')
    data = pd.read_csv(filename, delimiter=';')

    df = pd.DataFrame(data, columns=compact_columns_trips)

    # FIXME factprize
    return df


@pytest.fixture
def model_trips(source_data_trips, schema_trips):
    model = ModelBuilder().from_compact(source_data_trips) \
                          .with_schema(schema_trips) \
                          .render()
    return model


# networkx classes

class FlightInNode(InputNode):
    def __init__(self, properties):
        super().__init__(properties, 'flight_in', 'flight')


class FlightOutNode(OutputNode):
    def __init__(self, properties):
        super().__init__(properties, 'flight_out', 'flight')


@pytest.fixture
def class_mapping_trips():
    return {'area': AreaNode, 'country': CountryNode, 'town': TownNode,
            'flight_in': FlightInNode, 'flight_out': FlightOutNode}


@pytest.fixture
def graph_model_trips(class_mapping_trips, model_trips):
    graph_model = GraphBuilder().with_types(class_mapping_trips).with_model(model_trips).render()
    return graph_model


@pytest.fixture
def graph_style_trips(schema_trips):
    graph_style = StyleBuilder(schema_trips).render()
    return graph_style

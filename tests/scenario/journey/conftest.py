"""
Fixtures for
purpose : connected flights over multiple towns
The dataset has
- 3 levels : Country, Town
- 2 resources: monument, flight_in, flight_out
- flights in/out are connected
"""
import pytest
from os import path

import pandas as pd

# module import
from dependencynet.schema import SchemaBuilder
from dependencynet.model import ModelBuilder

from dependencynet.network.graphbuilder import LevelNode, ResourceNode, InputNode, OutputNode
from dependencynet.network.graphbuilder import GraphBuilder
from dependencynet.network.stylebuilder import StyleBuilder


@pytest.fixture
def schema_journey():
    schema = SchemaBuilder().level('country', 'C').level('town', 'T') \
                              .resource('monument', 'M', explode=True, delimiter=',') \
                              .resource('flight_in', 'FIn', role='INPUT', connect_id_name='flight') \
                              .resource('flight_out', 'FOut', role='OUTPUT', connect_id_name='flight') \
                              .connect('flight_out', 'flight_in') \
                              .render()
    return schema


@pytest.fixture(scope="session")
def compact_columns_journey():
    columns = ['country', 'town', 'monument', 'flight_in', 'flight_out']
    return columns


@pytest.fixture
def source_data_journey(schema_journey, compact_columns_journey):
    filename = path.join('tests', 'scenario', 'journey', 'resources', 'journey.csv')
    data = pd.read_csv(filename, delimiter=';')

    df = pd.DataFrame(data, columns=compact_columns_journey)

    # FIXME factprize
    return df


@pytest.fixture
def model_journey(source_data_journey, schema_journey):
    model = ModelBuilder().from_compact(source_data_journey) \
                          .with_schema(schema_journey) \
                          .render()

    return model


@pytest.fixture
def class_mapping_journey():
    return {'area': AreaNode, 'country': CountryNode, 'town': TownNode,
            'monument': MonumentNode,
            'flight_in': FlightInNode, 'flight_out': FlightOutNode}


# networkx classes

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


class FlightInNode(InputNode):
    def __init__(self, properties):
        super().__init__(properties, 'flight_in', 'flight')


class FlightOutNode(OutputNode):
    def __init__(self, properties):
        super().__init__(properties, 'flight_out', 'flight')


@pytest.fixture
def graph_model_journey(class_mapping_journey, model_journey):
    graph_model = GraphBuilder().with_types(class_mapping_journey).with_model(model_journey).render()
    return graph_model


@pytest.fixture
def graph_style_journey(schema_journey):
    graph_style = StyleBuilder(schema_journey).render()
    return graph_style

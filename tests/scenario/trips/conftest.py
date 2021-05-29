"""
Fixtures for trips
purpose : connected flights over multiple towns
The dataset has
- 3 levels : Area, Country, Town
- 2 resources: flight_in, flight_out
- flights in/out are connected
"""
import pytest
from os import path

import pandas as pd

# module import
from dependencynet.schema import SchemaBuilder
from dependencynet.model import ModelBuilder

from dependencynet.network.graphbuilder import LevelNode, InputNode, OutputNode


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
    filename = path.join('tests', 'scenario', 'trips', 'resources', 'trips.csv')
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


@pytest.fixture
def class_mapping_trips():
    return {'area': AreaNode, 'country': CountryNode, 'town': TownNode,
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


class FlightInNode(InputNode):
    def __init__(self, properties):
        super().__init__(properties, 'flight_in', 'flight')


class FlightOutNode(OutputNode):
    def __init__(self, properties):
        super().__init__(properties, 'flight_out', 'flight')

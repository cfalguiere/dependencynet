"""
This module tests the graph model - test cases : connection
"""
# third party import
import pytest

from os import path
import pandas as pd

from dependencynet.model import ModelBuilder

# module import
from dependencynet.network.graphbuilder import GraphBuilder, LevelNode
from dependencynet.network.graphbuilder import InputNode, OutputNode


@pytest.fixture
def source_data_trips(schema_trips, compact_columns_trips):
    filename = path.join('tests', 'resources', 'data', 'compact', 'trips.csv')
    data = pd.read_csv(filename, delimiter=';')

    df = pd.DataFrame(data, columns=compact_columns_trips)
    return df


@pytest.fixture
def model_trips(source_data_trips, schema_trips):
    model = ModelBuilder().from_compact(source_data_trips) \
                          .with_schema(schema_trips) \
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


# Tests
def test_graph_model(class_mapping_trips, model_trips):
    graph_model = GraphBuilder().with_types(class_mapping_trips).with_model(model_trips).render()
    assert graph_model

    lines = graph_model.pretty_print()

    # check connectionx out -> in on flights
    pattern = 'flight_out output resource %s -> flight_in input resource %s'
    assert len(lines) == 45
    link1 = pattern % ('A01C01T01FOut01', 'A02C01T01FIn01')
    link2 = pattern % ('A01C01T02FOut01', 'A01C03T01FIn01')
    link3 = pattern % ('A01C03T01FOut01', 'A01C01T01FIn01')
    link4 = pattern % ('A02C01T01FOut01', 'A01C02T01FIn01')
    assert lines[41] == link1
    assert lines[42] == link2
    assert lines[43] == link3
    assert lines[44] == link4


"""
utiliser trip
    def aggregate_level(self, levels_list):
    def merge_connection(self, left_name, right_name, connect_id_name):
        graph_model_3.merge_connection('flight_out', 'flight_in', 'flight')
    def fold_category(self, category, hide_inner=False):
    def summary(self):

"""

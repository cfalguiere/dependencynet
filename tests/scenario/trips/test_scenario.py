"""
Tests model creation using the dataset trips
TODO tests connect
TODO test viewer, graphml, style builder
"""
import pytest

# module import
from dependencynet.network.graphbuilder import GraphBuilder


@pytest.mark.trips
def test_schema_builder(schema_trips):
    a_schema = schema_trips
    # .resource('station', 'S') \  # FIXME  fixture is altered ?

    assert a_schema
    assert len(a_schema.levels['keys']) == 3
    assert len(a_schema.levels['marks']) == 3
    assert a_schema.levels['keys'][1] == 'country'
    assert a_schema.levels['marks'][1] == 'C'
    assert a_schema.resources['flight_in']['mark'] == 'FIn'
    assert a_schema.resources['flight_in']['explode'] is False

    # FIXME tests connect


@pytest.mark.trips
def test_model_builder(model_trips):
    model = model_trips

    assert model

    level_dfs = model.levels_datasets
    resource_dfs = model.resources_datasets

    assert len(level_dfs) == 3
    assert len(resource_dfs) == 2

    levels = ['area', 'country', 'town']

    df_area = level_dfs[0]
    assert df_area.shape == (2, 4)
    assert all(item in list(df_area.columns) for item in levels[0:0])
    assert df_area['label'][4] == 'A02 Asia'

    df_country = level_dfs[1]
    assert df_country.shape == (4, 6)
    assert all(item in list(df_country.columns) for item in levels[0:1])
    assert df_country['label'][2] == 'A01C03 Italia'

    df_town = level_dfs[2]
    assert df_town.shape == (5, 7)
    assert all(item in list(df_town.columns) for item in levels)
    assert df_town['label'][1] == 'A01C01T02 Lyon'

    df_flight_in = resource_dfs['flight_in']
    assert df_flight_in.shape == (4, 9)
    i_paris = 0
    assert all(item in list(df_flight_in.columns) for item in levels)
    assert all(item in list(df_flight_in.columns) for item in ['flight_in', 'flight'])
    assert df_flight_in['label'][i_paris] == 'A01C01T01FIn01 fl2'

    df_flight_out = resource_dfs['flight_out']
    assert df_flight_out.shape == (5, 9)
    i_paris = 0
    assert all(item in list(df_flight_out.columns) for item in levels)
    assert all(item in list(df_flight_out.columns) for item in ['flight_out', 'flight'])
    assert df_flight_out['label'][i_paris] == 'A01C01T01FOut01 fl3'


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
    assert link1 in lines
    assert link2 in lines
    assert link3 in lines
    assert link4 in lines


"""
utiliser trip
    def aggregate_level(self, levels_list):
    def merge_connection(self, left_name, right_name, connect_id_name):
        graph_model_3.merge_connection('flight_out', 'flight_in', 'flight')
    def fold_category(self, category, hide_inner=False):
    def summary(self):

"""

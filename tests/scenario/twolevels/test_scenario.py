"""
Tests model creation using the dataset towns
TODO test viewer, graphml
TODO test test_graph_model links monument
TODO test test_graph_model links level -> monument
"""
import pytest

import re

# module import
from dependencynet.network.graphbuilder import GraphBuilder
from dependencynet.network.stylebuilder import StyleBuilder


@pytest.mark.twolevels
def test_schema_builder(schema_towns):
    a_schema = schema_towns
    # .resource('station', 'S') \  # FIXME  fixture is altered ?

    assert a_schema
    assert len(a_schema.levels['keys']) == 2
    assert len(a_schema.levels['marks']) == 2
    assert a_schema.levels['keys'][0] == 'country'
    assert a_schema.levels['marks'][0] == 'C'
    assert a_schema.levels['keys'][1] == 'town'
    assert a_schema.levels['marks'][1] == 'T'
    assert a_schema.resources['monument']['mark'] == 'M'
    assert a_schema.resources['monument']['explode'] is True

    # FIXME tests connect


@pytest.mark.twolevels
def test_model_builder(model_towns):
    model = model_towns

    assert model

    level_dfs = model.levels_datasets
    resource_dfs = model.resources_datasets

    assert len(level_dfs) == 2
    assert len(resource_dfs) == 1

    levels = ['country', 'town']

    def has_levels(df, n=3):
        return all(item in list(df.columns) for item in levels[0:n-1])

    def has_resources(df, keys):
        return all(item in list(df.columns) for item in keys)

    df_country = level_dfs[0]
    assert df_country.shape == (4, 4)
    assert has_levels(df_country, 1)
    labels = df_country['label'].tolist()
    assert 'C01 France' in labels
    assert 'C02 UK' in labels
    assert 'C03 Italia' in labels
    assert 'C04 Japan' in labels

    df_town = level_dfs[1]
    assert df_town.shape == (5, 6)
    assert has_levels(df_town)
    labels = df_town['label'].tolist()
    assert 'C01T01 Paris' in labels
    assert 'C01T02 Lyon' in labels
    assert 'C02T01 London' in labels
    assert 'C03T01 Rome' in labels
    assert 'C04T01 Tokyo' in labels

    # WARNING order is not defined
    def select(s):
        return pattern.match(s)

    def extract_label(s):
        m = pattern.match(s)
        return m.group(1)

    df_monument = resource_dfs['monument']
    assert df_monument.shape == (6, 7)
    assert has_levels(df_monument)
    assert has_resources(df_monument, ['monument'])

    labels = df_monument['label'].tolist()
    pattern = re.compile(r"C\d{2}T\d{2}M\d{2} (.+)")
    selected = list(filter(pattern.match, labels))
    names = sorted([extract_label(s) for s in selected])
    assert names == sorted(['Eiffel Tower', 'Louvre Museum',
                            'Tower Bridge', 'Tower of London',
                            'Colosseum', 'Senso-ji'])


# Tests
@pytest.mark.twolevels
def test_graph_model(class_mapping_towns, model_towns):
    graph_model = GraphBuilder().with_types(class_mapping_towns).with_model(model_towns).render()
    assert graph_model

    lines = graph_model.pretty_print()
    assert len(lines) == 29

    pattern_level_country = 'country level - %s'
    for value in ['C01 France', 'C02 UK', 'C03 Italia',
                  'C04 Japan']:
        node = pattern_level_country % (value)
        assert node in lines

    pattern_level_town = 'town level - %s'
    for value in ['C01T01 Paris', 'C01T02 Lyon',
                  'C02T01 London',
                  'C03T01 Rome',
                  'C04T01 Tokyo']:
        node = pattern_level_town % (value)
        assert node in lines

    # WARNING order is not defined
    def select(s):
        return pattern.match(s)

    def extract_label(s):
        m = pattern.match(s)
        return m.group(1)

    pattern = re.compile(r"monument resource - C\d{2}T\d{2}M\d{2} (.+)")
    selected = list(filter(pattern.match, lines))
    names = sorted([extract_label(s) for s in selected])
    assert names == sorted(['Eiffel Tower', 'Louvre Museum',
                            'Tower Bridge', 'Tower of London',
                            'Colosseum', 'Senso-ji'])

    # check edges
    pattern = 'country level %s -> town level %s'
    edge = pattern % ('C01', 'C01T01')
    assert edge in lines
    edge = pattern % ('C01', 'C01T02')
    assert edge in lines
    edge = pattern % ('C02', 'C02T01')
    assert edge in lines
    edge = pattern % ('C03', 'C03T01')
    assert edge in lines
    edge = pattern % ('C04', 'C04T01')
    assert edge in lines

    pattern = 'town level %s -> monument resource %s'
    edge = pattern % ('C01T01', 'C01T01M01')
    assert edge in lines
    edge = pattern % ('C01T01', 'C01T01M02')
    assert edge in lines
    edge = pattern % ('C02T01', 'C02T01M01')
    assert edge in lines
    edge = pattern % ('C02T01', 'C02T01M02')
    assert edge in lines
    edge = pattern % ('C03T01', 'C03T01M01')
    assert edge in lines
    edge = pattern % ('C04T01', 'C04T01M01')
    assert edge in lines


@pytest.mark.twolevels
def test_graphstyle(schema_towns, compact_columns_towns):
    sb = StyleBuilder(schema_towns)
    graph_style = sb.render()

    selectors = [style['selector'] for style in graph_style]

    # check whether each node type is represented
    for element in compact_columns_towns:
        selector = f'node.{element}'
        assert selector in selectors
        i = selectors.index(selector)
        assert 'background-color' in graph_style[i]['css']
        assert 'color' in graph_style[i]['css']


"""
    def aggregate_level(self, levels_list):
    def merge_connection(self, left_name, right_name, connect_id_name):
        graph_model_3.merge_connection('flight_out', 'flight_in', 'flight')
    def fold_category(self, category, hide_inner=False):
    def summary(self):

"""

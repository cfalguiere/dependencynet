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


@pytest.mark.towns
def test_schema_builder(schema_towns):
    a_schema = schema_towns
    # .resource('station', 'S') \  # FIXME  fixture is altered ?

    assert a_schema
    assert len(a_schema.levels['keys']) == 3
    assert len(a_schema.levels['marks']) == 3
    assert a_schema.levels['keys'][0] == 'area'
    assert a_schema.levels['marks'][0] == 'A'
    assert a_schema.levels['keys'][1] == 'country'
    assert a_schema.levels['marks'][1] == 'C'
    assert a_schema.levels['keys'][2] == 'town'
    assert a_schema.levels['marks'][2] == 'T'
    assert a_schema.resources['monument']['mark'] == 'M'
    assert a_schema.resources['monument']['explode'] is True

    # FIXME tests connect


@pytest.mark.towns
def test_model_builder(model_towns):
    model = model_towns

    assert model

    level_dfs = model.levels_datasets
    resource_dfs = model.resources_datasets

    assert len(level_dfs) == 3
    assert len(resource_dfs) == 1

    levels = ['area', 'country', 'town']

    def has_levels(df, n=3):
        return all(item in list(df.columns) for item in levels[0:n-1])

    def has_resources(df, keys):
        return all(item in list(df.columns) for item in keys)

    df_area = level_dfs[0]
    assert df_area.shape == (2, 4)
    assert has_levels(df_area, 1)
    labels = df_area['label'].tolist()
    assert 'A01 Europe' in labels
    assert 'A02 Asia' in labels

    df_country = level_dfs[1]
    assert df_country.shape == (4, 6)
    assert has_levels(df_country, 2)
    labels = df_country['label'].tolist()
    assert 'A01C01 France' in labels
    assert 'A01C02 UK' in labels
    assert 'A01C03 Italia' in labels
    assert 'A02C01 Japan' in labels

    df_town = level_dfs[2]
    assert df_town.shape == (5, 7)
    assert has_levels(df_town)
    labels = df_town['label'].tolist()
    assert 'A01C01T01 Paris' in labels
    assert 'A01C01T02 Lyon' in labels
    assert 'A01C02T01 London' in labels
    assert 'A01C03T01 Rome' in labels
    assert 'A02C01T01 Tokyo' in labels

    # WARNING order is not defined
    def select(s):
        return pattern.match(s)

    def extract_label(s):
        m = pattern.match(s)
        return m.group(1)

    df_monument = resource_dfs['monument']
    assert df_monument.shape == (6, 8)
    assert has_levels(df_monument)
    assert has_resources(df_monument, ['monument'])

    labels = df_monument['label'].tolist()
    pattern = re.compile(r"A\d{2}C\d{2}T\d{2}M\d{2} (.+)")
    selected = list(filter(pattern.match, labels))
    names = sorted([extract_label(s) for s in selected])
    assert names == sorted(['Eiffel Tower', 'Louvre Museum',
                            'Tower Bridge', 'Tower of London',
                            'Colosseum', 'Senso-ji'])


# Tests
@pytest.mark.towns
def test_graph_model(class_mapping_towns, model_towns):
    graph_model = GraphBuilder().with_types(class_mapping_towns).with_model(model_towns).render()
    assert graph_model

    lines = graph_model.pretty_print()
    assert len(lines) == 35

    pattern_level_area = 'area level - %s'
    for value in ['A01 Europe', 'A02 Asia']:
        node = pattern_level_area % (value)
        assert node in lines

    pattern_level_country = 'country level - %s'
    for value in ['A01C01 France', 'A01C02 UK', 'A01C03 Italia',
                  'A02C01 Japan']:
        node = pattern_level_country % (value)
        assert node in lines

    pattern_level_town = 'town level - %s'
    for value in ['A01C01T01 Paris', 'A01C01T02 Lyon',
                  'A01C02T01 London',
                  'A01C03T01 Rome',
                  'A02C01T01 Tokyo']:
        node = pattern_level_town % (value)
        assert node in lines

    # WARNING order is not defined
    def select(s):
        return pattern.match(s)

    def extract_label(s):
        m = pattern.match(s)
        return m.group(1)

    pattern = re.compile(r"monument resource - A\d{2}C\d{2}T\d{2}M\d{2} (.+)")
    selected = list(filter(pattern.match, lines))
    names = sorted([extract_label(s) for s in selected])
    assert names == sorted(['Eiffel Tower', 'Louvre Museum',
                            'Tower Bridge', 'Tower of London',
                            'Colosseum', 'Senso-ji'])

    # check edges
    pattern = 'area level %s -> country level %s'
    edge = pattern % ('A01', 'A01C01')
    assert edge in lines
    edge = pattern % ('A01', 'A01C02')
    assert edge in lines
    edge = pattern % ('A01', 'A01C03')
    assert edge in lines
    edge = pattern % ('A02', 'A02C01')
    assert edge in lines

    pattern = 'country level %s -> town level %s'
    edge = pattern % ('A01C01', 'A01C01T01')
    assert edge in lines
    edge = pattern % ('A01C01', 'A01C01T02')
    assert edge in lines
    edge = pattern % ('A01C02', 'A01C02T01')
    assert edge in lines
    edge = pattern % ('A01C03', 'A01C03T01')
    assert edge in lines
    edge = pattern % ('A02C01', 'A02C01T01')
    assert edge in lines

    pattern = 'town level %s -> monument resource %s'
    edge = pattern % ('A01C01T01', 'A01C01T01M01')
    assert edge in lines
    edge = pattern % ('A01C01T01', 'A01C01T01M02')
    assert edge in lines
    edge = pattern % ('A01C02T01', 'A01C02T01M01')
    assert edge in lines
    edge = pattern % ('A01C02T01', 'A01C02T01M02')
    assert edge in lines
    edge = pattern % ('A01C03T01', 'A01C03T01M01')
    assert edge in lines
    edge = pattern % ('A02C01T01', 'A02C01T01M01')
    assert edge in lines


@pytest.mark.towns
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

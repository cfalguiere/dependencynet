"""
Tests model creation using the dataset journey
TODO test viewer, graphml
TODO test test_graph_model all node and links level -> resource
"""
import pytest

import re

from bs4 import BeautifulSoup

# module import
from dependencynet.network.graphbuilder import GraphBuilder
from dependencynet.network.stylebuilder import StyleBuilder
from dependencynet.network.graphviewer import GraphViewer
from dependencynet.network.graphml import GraphMLConverter


@pytest.mark.journey
def test_schema_builder(schema_journey):
    a_schema = schema_journey
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
    assert a_schema.resources['flight_in']['mark'] == 'FIn'
    assert a_schema.resources['flight_in']['explode'] is False
    assert a_schema.resources['flight_out']['mark'] == 'FOut'
    assert a_schema.resources['flight_out']['explode'] is False

    # FIXME tests connect


@pytest.mark.journey
def test_model_builder(model_journey):
    model = model_journey

    assert model

    level_dfs = model.levels_datasets
    resource_dfs = model.resources_datasets

    assert len(level_dfs) == 2
    assert len(resource_dfs) == 3

    levels = ['country', 'town']

    def has_levels(df, n=2):
        return all(item in list(df.columns) for item in levels[0:n-1])

    def has_resources(df, keys):
        return all(item in list(df.columns) for item in keys)

    df_country = level_dfs[0]
    assert df_country.shape == (4, 4)
    assert has_levels(df_country, 2)
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
                            'Tower Bridge', 'London Eye',
                            'Colosseum', 'Senso-ji'])

    df_flight_in = resource_dfs['flight_in']
    assert df_flight_in.shape == (4, 8)
    assert has_levels(df_flight_in)
    assert has_resources(df_flight_in, ['flight_in', 'flight'])
    labels = df_flight_in['label'].tolist()
    assert 'C01T01FIn01 fl2' in labels
    assert 'C02T01FIn01 fl4' in labels
    assert 'C03T01FIn01 fl1' in labels
    assert 'C04T01FIn01 fl3' in labels

    df_flight_out = resource_dfs['flight_out']
    assert df_flight_out.shape == (5, 8)
    assert has_levels(df_flight_out)
    assert has_resources(df_flight_out, ['flight_out', 'flight'])
    labels = df_flight_out['label'].tolist()
    assert 'C01T01FOut01 fl3' in labels
    assert 'C01T02FOut01 fl1' in labels
    assert 'C02T01FOut01 fl5' in labels
    assert 'C03T01FOut01 fl2' in labels
    assert 'C04T01FOut01 fl4' in labels


# Tests
@pytest.mark.journey
def test_graph_model(class_mapping_journey, model_journey):
    graph_model = GraphBuilder().with_types(class_mapping_journey).with_model(model_journey).render()
    assert graph_model

    lines = graph_model.pretty_print()
    assert len(lines) == 51

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
                            'Tower Bridge', 'London Eye',
                            'Colosseum', 'Senso-ji'])

    pattern_level_town = 'flight_in input resource - %s'
    for value in ['C01T01FIn01 fl2', 'C02T01FIn01 fl4',
                  'C03T01FIn01 fl1', 'C04T01FIn01 fl3']:
        node = pattern_level_town % (value)
        assert node in lines

    pattern_level_town = 'flight_out output resource - %s'
    for value in ['C01T01FOut01 fl3', 'C01T02FOut01 fl1', 'C02T01FOut01 fl5',
                  'C03T01FOut01 fl2', 'C04T01FOut01 fl4']:
        node = pattern_level_town % (value)
        assert node in lines

    # check edges
    pattern = 'country level %s -> town level %s'
    for pair in [('C01', 'C01T01'), ('C01', 'C01T02'),
                 ('C02', 'C02T01'), ('C03', 'C03T01'), ('C04', 'C04T01')]:
        edge = pattern % pair
        assert edge in lines

    pattern = 'town level %s -> monument resource %s'
    for pair in [('C01T01', 'C01T01M01'), ('C01T01', 'C01T01M02'),
                 ('C02T01', 'C02T01M01'), ('C02T01', 'C02T01M02'),
                 ('C03T01', 'C03T01M01'), ('C04T01', 'C04T01M01')]:
        edge = pattern % pair
        assert edge in lines

    pattern = 'town level %s -> flight_out output resource %s'
    for pair in [('C01T01', 'C01T01FOut01'), ('C01T02', 'C01T02FOut01'),
                 ('C02T01', 'C02T01FOut01'),
                 ('C03T01', 'C03T01FOut01'),
                 ('C04T01', 'C04T01FOut01')]:
        edge = pattern % pair
        assert edge in lines

    pattern = 'flight_in input resource %s -> town level %s'
    for pair in [('C01T01FIn01', 'C01T01'), ('C02T01FIn01', 'C02T01'),
                 ('C03T01FIn01', 'C03T01'), ('C04T01FIn01', 'C04T01')]:
        edge = pattern % pair
        assert edge in lines

    # check connectionx out -> in on flights
    pattern = 'flight_out output resource %s -> flight_in input resource %s'
    for pair in [('C01T01FOut01', 'C04T01FIn01'),
                 ('C01T02FOut01', 'C03T01FIn01'),
                 ('C03T01FOut01', 'C01T01FIn01'),
                 ('C04T01FOut01', 'C02T01FIn01')]:
        edge = pattern % pair
        assert edge in lines


@pytest.mark.journey
def test_graphstyle(schema_journey, compact_columns_journey):
    sb = StyleBuilder(schema_journey)
    graph_style = sb.render()

    selectors = [style['selector'] for style in graph_style]

    # check whether each node type is represented
    for element in compact_columns_journey:
        selector = f'node.{element}'
        assert selector in selectors
        i = selectors.index(selector)
        assert 'background-color' in graph_style[i]['css']
        assert 'color' in graph_style[i]['css']

    # check connection
    connect_selector = 'node.flight'
    assert connect_selector in selectors
    i = selectors.index(selector)
    assert 'background-color' in graph_style[i]['css']
    assert 'color' in graph_style[i]['css']


@pytest.mark.journey
def test_graph_viewer_journey(graph_model_journey, graph_style_journey):
    cytoscapeobj = GraphViewer(graph_model_journey).render('klay', graph_style_journey, 'LR')
    assert cytoscapeobj

    graph = cytoscapeobj.graph
    assert graph

    nb_country = 4
    nb_town = 5
    nb_monument = 6
    nb_flight_in = 4
    nb_flight_out = 5
    assert len(graph.nodes) == nb_country + nb_town + nb_monument + nb_flight_in + nb_flight_out

    nb_country_town = 5
    nb_flight_in_town = 4
    nb_town_flight_out = 5
    nb_town_monument = 6
    nb_flight_out_flight_in = 4
    nb = nb_country_town
    nb += nb_town_monument
    nb += nb_flight_in_town + nb_town_flight_out + nb_flight_out_flight_in
    assert len(graph.edges) == nb


@pytest.mark.journey
def test_graphml_converter_journey(schema_journey, graph_model_journey, graph_style_journey):
    converter = GraphMLConverter(graph_model_journey, graph_style_journey, schema_journey)
    graphml = converter.graphml_network.get_graph()
    assert graphml

    doc = BeautifulSoup(graphml, features="lxml")

    assert doc.graphml
    assert doc.graphml.find_all('key')[0]['for'] == 'node'
    assert doc.graphml.find_all('key')[5]['for'] == 'edge'

    assert doc.graphml.graph['edgedefault'] == 'directed'

    nodes = doc.graphml.graph.find_all('node')
    expected_nodes = [
        'C01', 'C02', 'C03', 'C04',
        'C01T01', 'C01T02', 'C02T01', 'C03T01', 'C04T01',
        'C01T01M01', 'C01T01M02', 'C02T01M01', 'C02T01M02', 'C03T01M01', 'C04T01M01',
        'C01T01FIn01', 'C02T01FIn01', 'C03T01FIn01', 'C04T01FIn01',
        'C01T01FOut01', 'C01T02FOut01', 'C02T01FOut01', 'C03T01FOut01', 'C04T01FOut01'
    ]
    assert len(nodes) == len(expected_nodes)
    node_ids = sorted([n['id'] for n in nodes])
    assert node_ids == sorted(expected_nodes)

    # TODO attributes et labels

    edges = doc.graphml.graph.find_all('edge')
    expected_edges = [
        ('C01', 'C01T01'),
        ('C01', 'C01T02'),
        ('C02', 'C02T01'),
        ('C03', 'C03T01'),
        ('C04', 'C04T01'),
        ('C01T01', 'C01T01M01'), ('C01T01', 'C01T01M02'),
        ('C02T01', 'C02T01M01'), ('C02T01', 'C02T01M02'),
        ('C03T01', 'C03T01M01'),
        ('C04T01', 'C04T01M01'),
        ('C01T01FIn01', 'C01T01'),
        ('C02T01FIn01', 'C02T01'),
        ('C03T01FIn01', 'C03T01'),
        ('C04T01FIn01', 'C04T01'),
        ('C01T01', 'C01T01FOut01'),
        ('C01T02', 'C01T02FOut01'),
        ('C02T01', 'C02T01FOut01'),
        ('C03T01', 'C03T01FOut01'),
        ('C04T01', 'C04T01FOut01'),
        ('C01T01FOut01', 'C04T01FIn01'),
        ('C01T02FOut01', 'C03T01FIn01'),
        ('C03T01FOut01', 'C01T01FIn01'),
        ('C04T01FOut01', 'C02T01FIn01')
    ]

    assert len(edges) == len(expected_edges)
    edge_pairs = sorted([(e['source'], e['target']) for e in edges])
    print(edge_pairs)
    print(sorted(expected_edges))
    assert edge_pairs == sorted(expected_edges)

"""
This module tests the feature remove_category of the graph model
after remove_category nodes of the type pass as parameter are removed
edges from this node are removed accordingly
limitation : can only remove upper level or levels
TODO test remove unexisting category, tests remove undefined category
TODO fix remove country or town with consistent edge remapping
"""
# third party import
import pytest

from bs4 import BeautifulSoup

from dependencynet.network.graphbuilder import GraphBuilder

# module import
from dependencynet.network.graphml import GraphMLConverter


# Tests
@pytest.mark.graphml
def test_remove_category_area(class_mapping_towns, model_towns, graph_style_towns, schema_towns):
    graph_model = GraphBuilder().with_types(class_mapping_towns).with_model(model_towns).render()
    assert graph_model

    graph_model.remove_category('area')

    lines = graph_model.pretty_print()
    assert len(lines) == 29

    converter = GraphMLConverter(graph_model, graph_style_towns, schema_towns)
    graphml = converter.graphml_network.get_graph()
    assert graphml

    doc = BeautifulSoup(graphml, features="lxml")

    assert doc.graphml
    assert doc.graphml.find_all('key')[0]['for'] == 'node'
    assert doc.graphml.find_all('key')[5]['for'] == 'edge'

    assert doc.graphml.graph['edgedefault'] == 'directed'

    nodes = doc.graphml.graph.find_all('node')
    expected_nodes = [
        'A01C01', 'A01C02', 'A01C03', 'A02C01',
        'A01C01T01', 'A01C01T02', 'A01C02T01', 'A01C03T01', 'A02C01T01',
        'A01C01T01M01', 'A01C01T01M02', 'A01C02T01M01', 'A01C02T01M02', 'A01C03T01M01', 'A02C01T01M01'
    ]
    assert len(nodes) == len(expected_nodes)
    node_ids = sorted([n['id'] for n in nodes])
    assert node_ids == sorted(expected_nodes)

    # TODO attributes et labels

    edges = doc.graphml.graph.find_all('edge')
    expected_edges = [
        ('A01C01', 'A01C01T01'),
        ('A01C01', 'A01C01T02'),
        ('A01C02', 'A01C02T01'),
        ('A01C03', 'A01C03T01'),
        ('A02C01', 'A02C01T01'),
        ('A01C01T01', 'A01C01T01M01'),
        ('A01C01T01', 'A01C01T01M02'),
        ('A01C02T01', 'A01C02T01M01'),
        ('A01C02T01', 'A01C02T01M02'),
        ('A01C03T01', 'A01C03T01M01'),
        ('A02C01T01', 'A02C01T01M01')
    ]
    assert len(edges) == len(expected_edges)
    edge_pairs = sorted([(e['source'], e['target']) for e in edges])
    assert edge_pairs == sorted(expected_edges)


# Tests
@pytest.mark.graphml
def test_remove_category_area_country(class_mapping_towns, model_towns, graph_style_towns, schema_towns):
    graph_model = GraphBuilder().with_types(class_mapping_towns).with_model(model_towns).render()
    assert graph_model

    graph_model.remove_category('area')
    graph_model.remove_category('country')

    lines = graph_model.pretty_print()
    assert len(lines) == 20

    converter = GraphMLConverter(graph_model, graph_style_towns, schema_towns)
    graphml = converter.graphml_network.get_graph()
    assert graphml

    doc = BeautifulSoup(graphml, features="lxml")

    assert doc.graphml
    assert doc.graphml.find_all('key')[0]['for'] == 'node'
    assert doc.graphml.find_all('key')[5]['for'] == 'edge'

    assert doc.graphml.graph['edgedefault'] == 'directed'

    nodes = doc.graphml.graph.find_all('node')
    expected_nodes = [
        'A01C01T01', 'A01C01T02', 'A01C02T01', 'A01C03T01', 'A02C01T01',
        'A01C01T01M01', 'A01C01T01M02', 'A01C02T01M01', 'A01C02T01M02', 'A01C03T01M01', 'A02C01T01M01'
    ]
    assert len(nodes) == len(expected_nodes)
    node_ids = sorted([n['id'] for n in nodes])
    assert node_ids == sorted(expected_nodes)

    # TODO attributes et labels

    edges = doc.graphml.graph.find_all('edge')
    expected_edges = [
        ('A01C01T01', 'A01C01T01M01'),
        ('A01C01T01', 'A01C01T01M02'),
        ('A01C02T01', 'A01C02T01M01'),
        ('A01C02T01', 'A01C02T01M02'),
        ('A01C03T01', 'A01C03T01M01'),
        ('A02C01T01', 'A02C01T01M01')
    ]
    assert len(edges) == len(expected_edges)
    edge_pairs = sorted([(e['source'], e['target']) for e in edges])
    assert edge_pairs == sorted(expected_edges)

"""
This module tests the graphml converter
TODO tests after graph manipulation
"""
# third party import
import pytest

from bs4 import BeautifulSoup

# module import
from dependencynet.network.graphml import GraphMLConverter


@pytest.mark.graphml
def test_graphml_converter_towns(schema_towns, graph_model_towns, graph_style_towns):
    converter = GraphMLConverter(graph_model_towns, graph_style_towns, schema_towns)
    graphml = converter.graphml_network.get_graph()
    assert graphml

    doc = BeautifulSoup(graphml, features="lxml")

    assert doc.graphml
    assert doc.graphml.find_all('key')[0]['for'] == 'node'
    assert doc.graphml.find_all('key')[5]['for'] == 'edge'

    assert doc.graphml.graph['edgedefault'] == 'directed'

    nodes = doc.graphml.graph.find_all('node')
    expected_nodes = [
        'A01', 'A02',
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
        ('A01', 'A01C01'),
        ('A01', 'A01C02'),
        ('A01', 'A01C03'),
        ('A02', 'A02C01'),
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


@pytest.mark.graphml
def test_graphml_converter_trips(schema_trips, graph_model_trips, graph_style_trips):
    converter = GraphMLConverter(graph_model_trips, graph_style_trips, schema_trips)
    graphml = converter.graphml_network.get_graph()
    assert graphml

    doc = BeautifulSoup(graphml, features="lxml")

    assert doc.graphml
    assert doc.graphml.find_all('key')[0]['for'] == 'node'
    assert doc.graphml.find_all('key')[5]['for'] == 'edge'

    assert doc.graphml.graph['edgedefault'] == 'directed'

    nodes = doc.graphml.graph.find_all('node')
    expected_nodes = [
        'A01', 'A02',
        'A01C01', 'A01C02', 'A01C03', 'A02C01',
        'A01C01T01', 'A01C01T02', 'A01C02T01', 'A01C03T01', 'A02C01T01',
        'A01C01T01FIn01', 'A01C02T01FIn01', 'A01C03T01FIn01', 'A02C01T01FIn01',
        'A01C01T01FOut01', 'A01C01T02FOut01', 'A01C02T01FOut01', 'A01C03T01FOut01', 'A02C01T01FOut01'
    ]
    assert len(nodes) == len(expected_nodes)
    node_ids = sorted([n['id'] for n in nodes])
    assert node_ids == sorted(expected_nodes)

    # TODO attributes et labels

    edges = doc.graphml.graph.find_all('edge')
    expected_edges = [
        ('A01', 'A01C01'),
        ('A01', 'A01C02'),
        ('A01', 'A01C03'),
        ('A02', 'A02C01'),
        ('A01C01', 'A01C01T01'),
        ('A01C01', 'A01C01T02'),
        ('A01C02', 'A01C02T01'),
        ('A01C03', 'A01C03T01'),
        ('A02C01', 'A02C01T01'),
        ('A01C01T01FIn01', 'A01C01T01'),
        ('A01C02T01FIn01', 'A01C02T01'),
        ('A01C03T01FIn01', 'A01C03T01'),
        ('A02C01T01FIn01', 'A02C01T01'),
        ('A01C01T01', 'A01C01T01FOut01'),
        ('A01C01T02', 'A01C01T02FOut01'),
        ('A01C02T01', 'A01C02T01FOut01'),
        ('A01C03T01', 'A01C03T01FOut01'),
        ('A02C01T01', 'A02C01T01FOut01'),
        ('A01C01T01FOut01', 'A02C01T01FIn01'),
        ('A01C01T02FOut01', 'A01C03T01FIn01'),
        ('A01C03T01FOut01', 'A01C01T01FIn01'),
        ('A02C01T01FOut01', 'A01C02T01FIn01')
    ]

    assert len(edges) == len(expected_edges)
    edge_pairs = sorted([(e['source'], e['target']) for e in edges])
    print(edge_pairs)
    print(sorted(expected_edges))
    assert edge_pairs == sorted(expected_edges)

"""
This module tests fold_category of the graph model
after fold_category flight
- town -> flight -> town
- becomes town -> town
after fold_category town
- town -> flight -> town
- becomes flight  -> flight
TODO when no merge ahead
TODO wrong attributes
TODO scenario open
"""
# third party import
import pytest

from bs4 import BeautifulSoup

from dependencynet.network.graphbuilder import GraphBuilder

# module import
from dependencynet.network.graphml import GraphMLConverter


@pytest.mark.graphml
@pytest.mark.trips
def test_fold_categpry_flight(class_mapping_trips, model_trips, graph_style_trips, schema_trips):
    graph_model = GraphBuilder().with_types(class_mapping_trips).with_model(model_trips).render()
    assert graph_model

    graph_model.merge_connection('flight_out', 'flight_in', 'flight')
    graph_model.fold_category('flight')

    lines = graph_model.pretty_print()
    assert len(lines) == 27

    converter = GraphMLConverter(graph_model, graph_style_trips, schema_trips)
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
        'A01C01T01', 'A01C01T02', 'A01C02T01', 'A01C03T01', 'A02C01T01'
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
        ('A01C01T01', 'A02C01T01'),
        ('A01C01T02', 'A01C03T01'),
        ('A01C03T01', 'A01C01T01'),
        ('A02C01T01', 'A01C02T01')
    ]
    assert len(edges) == len(expected_edges)
    edge_pairs = sorted([(e['source'], e['target']) for e in edges])
    assert edge_pairs == sorted(expected_edges)


@pytest.mark.graphml
@pytest.mark.trips
def test_fold_categpry_town(class_mapping_trips, model_trips, graph_style_trips, schema_trips):
    graph_model = GraphBuilder().with_types(class_mapping_trips).with_model(model_trips).render()
    assert graph_model

    graph_model.merge_connection('flight_out', 'flight_in', 'flight')
    graph_model.fold_category('town')

    lines = graph_model.pretty_print()
    assert len(lines) == 24

    converter = GraphMLConverter(graph_model, graph_style_trips, schema_trips)
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
        'fl1', 'fl2', 'fl3', 'fl4'
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
        ('A01C01', 'fl1'), ('A01C01', 'fl3'),
        ('A01C03', 'fl2'),
        ('A02C01', 'fl4'),
        ('fl3', 'fl4'),
        ('fl1', 'fl2'),
        ('fl2', 'fl3')
    ]
    assert len(edges) == len(expected_edges)
    edge_pairs = sorted([(e['source'], e['target']) for e in edges])
    assert edge_pairs == sorted(expected_edges)

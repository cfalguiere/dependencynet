"""
Tests model creation using the dataset libs
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


@pytest.mark.libs
def test_schema_builder(schema_libs):
    a_schema = schema_libs
    # .resource('station', 'S') \  # FIXME  fixture is altered ?

    assert a_schema
    assert len(a_schema.levels['keys']) == 0
    assert a_schema.resources['subsystem']['mark'] == 'S'
    assert a_schema.resources['artefact']['mark'] == 'A'
    assert a_schema.resources['repository']['mark'] == 'R'


@pytest.mark.libs
def test_model_builder(model_libs):
    model = model_libs

    assert model
    assert model.is_empty


# Tests
@pytest.mark.libs
def test_graph_model(graph_model_libs):
    assert graph_model_libs

    lines = graph_model_libs.pretty_print()
    assert len(lines) == 20

    pattern_system = 'subsystem resource - %s'
    for value in ['Web Site Gui', 'Web Site API', 'IAM Service']:
        node = pattern_system % (value)
        assert node in lines

    pattern_artefact = 'artefact resource - %s'
    for value in ['web-site-gui:v1.5.2', 'vue-js:3.0.11',
                  'web-site-api:v1.8.1', 'flask:2.0.1']:
        node = pattern_artefact % (value)
        assert node in lines

    pattern_repository = 'repository resource - %s'
    for value in ['web/front', 'web/back']:
        node = pattern_repository % (value)
        assert node in lines

    # check edges
    print(lines)

    pattern = 'subsystem resource %s -> subsystem resource %s'
    for pair in [('Sgui', 'Sapi'), ('Sapi', 'Siam')]:
        edge = pattern % pair
        assert edge in lines

    pattern = 'subsystem resource %s -> artefact resource %s'
    for pair in [('Sgui', 'Agui'), ('Sapi', 'Aapi')]:
        edge = pattern % pair
        assert edge in lines

    pattern = 'artefact resource %s -> artefact resource %s'
    for pair in [('Agui', 'Avue'), ('Aapi', 'Arest')]:
        edge = pattern % pair
        assert edge in lines

    pattern = 'artefact resource %s -> repository resource %s'
    for pair in [('Agui', 'Rfront'), ('Aapi', 'Rback')]:
        edge = pattern % pair
        assert edge in lines


@pytest.mark.libs
def test_graphstyle(schema_libs):
    sb = StyleBuilder(schema_libs)
    graph_style = sb.render()

    selectors = [style['selector'] for style in graph_style]

    # check whether each node type is represented
    for element in ['subsystem', 'artefact', 'repository']:
        selector = f'node.{element}'
        assert selector in selectors
        i = selectors.index(selector)
        assert 'background-color' in graph_style[i]['css']
        assert 'color' in graph_style[i]['css']


@pytest.mark.libs
def test_graph_viewer_libs(graph_model_libs, graph_style_libs):
    cytoscapeobj = GraphViewer(graph_model_libs).render('klay', graph_style_libs, 'LR')
    assert cytoscapeobj

    graph = cytoscapeobj.graph
    assert graph

    nb_subsystem = 3
    nb_artefact = 4
    nb_repository = 2
    assert len(graph.nodes) == nb_subsystem + nb_artefact + nb_repository

    nb_subsystem_artefact = 4
    nb_artefact_artefact = 2
    nb_artefact_repository = 2
    nb = nb_subsystem_artefact + nb_artefact_artefact + nb_artefact_repository
    assert len(graph.edges) == nb


@pytest.mark.libs
def test_graphml_converter_libs(schema_libs, graph_model_libs, graph_style_libs):
    converter = GraphMLConverter(graph_model_libs, graph_style_libs, schema_libs)
    graphml = converter.graphml_network.get_graph()
    assert graphml

    doc = BeautifulSoup(graphml, features="lxml")

    assert doc.graphml
    assert doc.graphml.find_all('key')[0]['for'] == 'node'
    assert doc.graphml.find_all('key')[5]['for'] == 'edge'

    assert doc.graphml.graph['edgedefault'] == 'directed'

    nodes = doc.graphml.graph.find_all('node')
    expected_nodes = [
        'Sgui', 'Sapi', 'Siam',
        'Agui', 'Avue', 'Aapi', 'Arest',
        'Rfront', 'Rback'
    ]
    assert len(nodes) == len(expected_nodes)
    node_ids = sorted([n['id'] for n in nodes])
    assert node_ids == sorted(expected_nodes)

    # TODO attributes et labels

    edges = doc.graphml.graph.find_all('edge')
    expected_edges = [
        ('Sgui', 'Sapi'),
        ('Sapi', 'Siam'),
        ('Sgui', 'Agui'),
        ('Sapi', 'Aapi'),
        ('Agui', 'Avue'),
        ('Aapi', 'Arest'),
        ('Agui', 'Rfront'),
        ('Aapi', 'Rback')
    ]

    assert len(edges) == len(expected_edges)
    edge_pairs = sorted([(e['source'], e['target']) for e in edges])
    print(edge_pairs)
    print(sorted(expected_edges))
    assert edge_pairs == sorted(expected_edges)

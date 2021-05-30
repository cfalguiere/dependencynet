"""
This module tests the ipycytocscape vonverter
TODO tests after graph manipulation
"""
# third party import
import pytest

# module import
from dependencynet.network.graphviewer import GraphViewer


@pytest.mark.graph_viewer
def test_graph_viewer_towns(graph_model_towns, graph_style_towns):
    print('about to create viewer')
    cytoscapeobj = GraphViewer(graph_model_towns).render('klay', graph_style_towns, 'LR')
    assert cytoscapeobj

    graph = cytoscapeobj.graph
    assert graph

    nb_area = 2
    nb_country = 4
    nb_town = 5
    nb_monument = 6
    assert len(graph.nodes) == nb_area + nb_country + nb_town + nb_monument

    nb_area_country = 4
    nb_country_town = 5
    nb_town_monument = 6
    assert len(graph.edges) == nb_area_country + nb_country_town + nb_town_monument


@pytest.mark.graph_viewer
def test_graph_viewer_trips(graph_model_trips, graph_style_trips):
    cytoscapeobj = GraphViewer(graph_model_trips).render('klay', graph_style_trips, 'LR')
    assert cytoscapeobj

    graph = cytoscapeobj.graph
    assert graph

    nb_area = 2
    nb_country = 4
    nb_town = 5
    nb_flight_in = 4
    nb_flight_out = 5
    assert len(graph.nodes) == nb_area + nb_country + nb_town + nb_flight_in + nb_flight_out

    nb_area_country = 4
    nb_country_town = 5
    nb_flight_in_town = 4
    nb_town_flight_out = 5
    nb_flight_out_flight_in = 4
    nb = nb_area_country + nb_country_town
    nb += nb_flight_in_town + nb_town_flight_out + nb_flight_out_flight_in
    assert len(graph.edges) == nb

"""
This module tests merge_connection of the graph model
TODO merge when wrong attributes, or no connection in schema (need other dataset)
"""
# third party import
import pytest


# module import
from dependencynet.network.graphbuilder import GraphBuilder


@pytest.mark.graph_model
@pytest.mark.trips
def test_merge_connections(class_mapping_trips, model_trips):
    graph_model = GraphBuilder().with_types(class_mapping_trips).with_model(model_trips).render()
    assert graph_model

    graph_model.merge_connection('flight_out', 'flight_in', 'flight')

    lines = graph_model.pretty_print()
    assert len(lines) == 35

    pattern_level_flight = 'flight level - %s'
    for value in ['fl1', 'fl2', 'fl3', 'fl4']:
        node = pattern_level_flight % (value)
        assert node in lines

    # check edges

    pattern = 'town level %s -> flight resource %s'
    for pair in [('A01C01T01', 'fl3'),
                 ('A01C01T02', 'fl1'),
                 ('A01C03T01', 'fl2'),
                 ('A02C01T01', 'fl4')]:
        edge = pattern % pair
        assert edge in lines

    pattern = 'flight output resource %s -> town level %s'
    for pair in [('fl3', 'A02C01T01'),
                 ('fl1', 'A01C03T01'),
                 ('fl2', 'A01C01T01'),
                 ('fl4', 'A01C02T01')]:
        edge = pattern % pair
        assert edge in lines

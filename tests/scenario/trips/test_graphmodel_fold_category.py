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

import re

# module import
from dependencynet.network.graphbuilder import GraphBuilder


@pytest.mark.graph_model
@pytest.mark.trips
def test_fold_categpry_flight(class_mapping_trips, model_trips):
    graph_model = GraphBuilder().with_types(class_mapping_trips).with_model(model_trips).render()
    assert graph_model

    graph_model.merge_connection('flight_out', 'flight_in', 'flight')
    graph_model.fold_category('flight')

    lines = graph_model.pretty_print()
    assert len(lines) == 27

    pattern_level_town = 'town level - %s'
    for value in ['A01C01T01 Paris', 'A01C02T01 London',
                  'A01C03T01 Rome', 'A02C01T01 Tokyo']:
        node = pattern_level_town % (value)
        assert node in lines

    pattern = re.compile(r"flight resource  - (.+)")
    selected = list(filter(pattern.match, lines))
    assert len(selected) == 0

    # check edges

    pattern = 'town level %s -> town level %s'
    for pair in [('A01C01T01', 'A02C01T01'),
                 ('A01C01T02', 'A01C03T01'),
                 ('A01C03T01', 'A01C01T01'),
                 ('A02C01T01', 'A01C02T01')]:
        edge = pattern % pair
        assert edge in lines


@pytest.mark.graph_model
@pytest.mark.trips
def test_fold_categpry_town(class_mapping_trips, model_trips):
    graph_model = GraphBuilder().with_types(class_mapping_trips).with_model(model_trips).render()
    assert graph_model

    graph_model.merge_connection('flight_out', 'flight_in', 'flight')
    graph_model.fold_category('town')

    lines = graph_model.pretty_print()
    assert len(lines) == 24

    pattern_level_flight = 'flight resource - %s'
    for value in ['fl1', 'fl2', 'fl3', 'fl4']:
        node = pattern_level_flight % (value)
        assert node in lines

    pattern = re.compile(r"town level  - (.+)")
    selected = list(filter(pattern.match, lines))
    assert len(selected) == 0

    # check edges

    pattern = 'flight resource %s -> flight resource %s'
    for pair in [('fl3', 'fl4'),
                 ('fl1', 'fl2'),
                 ('fl2', 'fl3')]:
        edge = pattern % pair
        assert edge in lines

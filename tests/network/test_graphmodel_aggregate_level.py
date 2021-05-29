"""
This module tests the feature aggregate_level of the graph model
after aggregate_level keeps only level nodes and aggregate resources in remaining nodes
edges are removed accordingly
limitation : can only aggregate upper levels
TODO test aggregate_level for unknown level, or non ordered levels
"""
# third party import
import pytest

import re

# module import
from dependencynet.network.graphbuilder import GraphBuilder


# Tests
@pytest.mark.graph_model
def test_aggregate_level_area_country(class_mapping_towns, model_towns):
    graph_model = GraphBuilder().with_types(class_mapping_towns).with_model(model_towns).render()
    assert graph_model

    graph_model.aggregate_level(['area', 'country'])

    lines = graph_model.pretty_print()
    assert len(lines) == 25

    pattern_level_area = 'area level - %s'
    for value in ['A01 Europe', 'A02 Asia']:
        node = pattern_level_area % (value)
        assert node in lines

    pattern_level_country = 'country level - %s'
    for value in ['A01C01 France', 'A01C02 UK', 'A01C03 Italia',
                  'A02C01 Japan']:
        node = pattern_level_country % (value)
        assert node in lines

    pattern = re.compile(r"(.*)town level(.*)")
    selected = list(filter(pattern.match, lines))
    assert len(selected) == 0

    pattern = 'area level %s -> country level %s'
    for pair in [('A01', 'A01C01'), ('A01', 'A01C02'),
                 ('A01', 'A01C03'),
                 ('A02', 'A02C01')]:
        edge = pattern % pair
        assert edge in lines

    pattern = 'country level %s -> monument resource %s'
    for pair in [('A01C01', 'A01C01T01M01'), ('A01C01', 'A01C01T01M02'),
                 ('A01C02', 'A01C02T01M01'), ('A01C02', 'A01C02T01M02'),
                 ('A01C03', 'A01C03T01M01'),
                 ('A02C01', 'A02C01T01M01')]:
        edge = pattern % pair
        assert edge in lines


# Tests
@pytest.mark.graph_model
def test_aggregate_level_area(class_mapping_towns, model_towns):
    graph_model = GraphBuilder().with_types(class_mapping_towns).with_model(model_towns).render()
    assert graph_model

    graph_model.aggregate_level(['area'])

    lines = graph_model.pretty_print()
    assert len(lines) == 17

    pattern_level_area = 'area level - %s'
    for value in ['A01 Europe', 'A02 Asia']:
        node = pattern_level_area % (value)
        assert node in lines

    pattern = re.compile(r"(.*)country level(.*)")
    selected = list(filter(pattern.match, lines))
    assert len(selected) == 0

    pattern = re.compile(r"(.*)town level(.*)")
    selected = list(filter(pattern.match, lines))
    assert len(selected) == 0

    pattern = 'area level %s -> monument resource %s'
    for pair in [('A01', 'A01C01T01M01'), ('A01', 'A01C01T01M02'),
                 ('A01', 'A01C02T01M01'), ('A01', 'A01C02T01M02'),
                 ('A01', 'A01C03T01M01'),
                 ('A02', 'A02C01T01M01')]:
        edge = pattern % pair
        assert edge in lines

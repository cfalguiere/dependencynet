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

import re

# module import
from dependencynet.network.graphbuilder import GraphBuilder


# Tests
@pytest.mark.graph_model
def test_remove_category_area(class_mapping_towns, model_towns):
    graph_model = GraphBuilder().with_types(class_mapping_towns).with_model(model_towns).render()
    assert graph_model

    graph_model.remove_category('area')

    lines = graph_model.pretty_print()
    assert len(lines) == 29

    pattern = re.compile(r"area level - (.+)")
    selected = list(filter(pattern.match, lines))
    assert len(selected) == 0

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

    pattern = 'country level %s -> town level %s'
    for pair in [('A01C01', 'A01C01T01'), ('A01C01', 'A01C01T02'),
                 ('A01C02', 'A01C02T01'),
                 ('A01C03', 'A01C03T01'),
                 ('A02C01', 'A02C01T01')]:
        edge = pattern % pair
        assert edge in lines

    pattern = 'town level %s -> monument resource %s'
    for pair in [('A01C01T01', 'A01C01T01M01'), ('A01C01T01', 'A01C01T01M02'),
                 ('A01C02T01', 'A01C02T01M01'), ('A01C02T01', 'A01C02T01M02'),
                 ('A01C03T01', 'A01C03T01M01'),
                 ('A02C01T01', 'A02C01T01M01')]:
        edge = pattern % pair
        assert edge in lines


# Tests
@pytest.mark.graph_model
def test_remove_category_area_country(class_mapping_towns, model_towns):
    graph_model = GraphBuilder().with_types(class_mapping_towns).with_model(model_towns).render()
    assert graph_model

    graph_model.remove_category('area')
    graph_model.remove_category('country')

    lines = graph_model.pretty_print()
    assert len(lines) == 20

    pattern = re.compile(r"(.*)area level(.*)")
    selected = list(filter(pattern.match, lines))
    assert len(selected) == 0

    pattern = re.compile(r"(.*)country level(.*)")
    selected = list(filter(pattern.match, lines))
    assert len(selected) == 0

    pattern_level_town = 'town level - %s'
    for value in ['A01C01T01 Paris', 'A01C01T02 Lyon',
                  'A01C02T01 London',
                  'A01C03T01 Rome',
                  'A02C01T01 Tokyo']:
        node = pattern_level_town % (value)
        assert node in lines

    # check edges
    pattern = 'town level %s -> monument resource %s'
    for pair in [('A01C01T01', 'A01C01T01M01'), ('A01C01T01', 'A01C01T01M02'),
                 ('A01C02T01', 'A01C02T01M01'), ('A01C02T01', 'A01C02T01M02'),
                 ('A01C03T01', 'A01C03T01M01'),
                 ('A02C01T01', 'A02C01T01M01')]:
        edge = pattern % pair
        assert edge in lines


# Tests
@pytest.mark.graph_model
def xtest_remove_category_country(class_mapping_towns, model_towns):
    "cannot remove arbitrary level - edges are not set"
    graph_model = GraphBuilder().with_types(class_mapping_towns).with_model(model_towns).render()
    assert graph_model

    graph_model.remove_category('country')

    lines = graph_model.pretty_print()
    assert len(lines) == 22

    print(lines)

    pattern_level_area = 'area level - %s'
    for value in ['A01 Europe', 'A02 Asia']:
        node = pattern_level_area % (value)
        assert node in lines

    pattern_level_town = 'town level - %s'
    for value in ['A01C01T01 Paris', 'A01C01T02 Lyon',
                  'A01C02T01 London',
                  'A01C03T01 Rome',
                  'A02C01T01 Tokyo']:
        node = pattern_level_town % (value)
        assert node in lines

    # check edges
    pattern = 'area level %s -> country level %s'
    for pair in [('A01', 'A01C01'), ('A01', 'A01C02'),
                 ('A01', 'A01C03'),
                 ('A02', 'A02C01')]:
        edge = pattern % pair
        assert edge in lines

    pattern = 'area level %s -> town level %s'
    for pair in [('A01', 'A01C01T01'), ('A01', 'A01C01T02'),
                 ('A01', 'A01C02T01'),
                 ('A01', 'A01C03T01'),
                 ('A02', 'A02C01T01')]:
        edge = pattern % pair
        assert edge in lines

    pattern = 'town level %s -> monument resource %s'
    for pair in [('A01C01T01', 'A01C01T01M01'), ('A01C01T01', 'A01C01T01M02'),
                 ('A01C02T01', 'A01C02T01M01'), ('A01C02T01', 'A01C02T01M02'),
                 ('A01C03T01', 'A01C03T01M01'),
                 ('A02C01T01', 'A02C01T01M01')]:
        edge = pattern % pair
        assert edge in lines

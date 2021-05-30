"""
This module tests the graph model
"""
# third party import
import pytest

import re

# module import
from dependencynet.network.graphbuilder import GraphBuilder


@pytest.mark.graph_model
def test_graph_model(class_mapping_towns, model_towns):
    graph_model = GraphBuilder().with_types(class_mapping_towns).with_model(model_towns).render()
    assert graph_model

    lines = graph_model.pretty_print()
    assert len(lines) == 35

    pattern_level_area = 'area level - %s'
    for value in ['A01 Europe', 'A02 Asia']:
        node = pattern_level_area % (value)
        assert node in lines

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

    # WARNING order is not defined
    def select(s):
        return pattern.match(s)

    def extract_label(s):
        m = pattern.match(s)
        return m.group(1)

    pattern = re.compile(r"monument resource - A\d{2}C\d{2}T\d{2}M\d{2} (.+)")
    selected = list(filter(pattern.match, lines))
    names = sorted([extract_label(s) for s in selected])
    assert names == sorted(['Eiffel Tower', 'Louvre Museum',
                            'Tower Bridge', 'Tower of London',
                            'Colosseum', 'Senso-ji'])

    # check edges
    pattern = 'area level %s -> country level %s'
    for pair in [('A01', 'A01C01'), ('A01', 'A01C02'),
                 ('A01', 'A01C03'),
                 ('A02', 'A02C01')]:
        edge = pattern % pair
        assert edge in lines

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


@pytest.mark.graph_model
def test_summary(class_mapping_towns, model_towns):
    graph_model = GraphBuilder().with_types(class_mapping_towns).with_model(model_towns).render()
    assert graph_model

    counts = graph_model.summary()

    print(counts)

    assert counts['area level'] == 2
    assert counts['country level'] == 4
    assert counts['town level'] == 5

    assert counts['monument resource'] == 6

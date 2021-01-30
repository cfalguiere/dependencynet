# third party import
import pytest

import logging
from os import path

import pandas as pd

# module import
from dependencynet.datasets_utils import extract_hierarchy
from dependencynet.trees_utils import build_tree, pretty_print_tree


@pytest.fixture
def logger():
    logging.basicConfig()
    logger = logging.getLogger('test_datasets_utils')
    logger.setLevel(logging.WARN)


@pytest.fixture
def keys_towns():
    keys = ['area', 'country', 'town']
    return keys


@pytest.fixture
def tree_datasets_towns(keys_towns):
    filename = path.join('tests', 'resources', 'data', 'compact', 'towns.csv')
    data = pd.read_csv(filename, delimiter=';')

    df = pd.DataFrame(data, columns=keys_towns)

    marks = "ACT"
    dfs = extract_hierarchy(df, keys_towns, marks)

    return dfs


# Tests
def test_build_tree_towns(tree_datasets_towns, keys_towns, logger):
    tree = build_tree(tree_datasets_towns, keys_towns)

    assert tree
    assert len(tree['area_dict']) == 2
    a1 = tree['area_dict']['A01']
    assert len(a1['country_dict']) == 3
    a1c1 = a1['country_dict']['A01C01']
    assert len(a1c1['town_dict']) == 2
    a1c1t2 = a1c1['town_dict']['A01C01T02']
    assert a1c1t2['area'] == 'Europe'
    assert a1c1t2['country'] == 'France'
    assert a1c1t2['town'] == 'Lyon'


# Tests
def test_pretty_print_tree(tree_datasets_towns, keys_towns, logger):
    tree = build_tree(tree_datasets_towns, keys_towns)
    lines = pretty_print_tree(tree, keys_towns)

    assert len(lines) == 25
    assert lines[0] == 'there are 2 area(s)'
    assert lines[1] == '  A01, A02'
    assert lines[2] == '  area A01: Europe'
    assert lines[3] == '    has 3 country(s)'
    assert lines[4] == '      A01C01, A01C02, A01C03'
    assert lines[5] == '      country A01C01: France'
    assert lines[6] == '        has 2 town(s)'
    assert lines[7] == '          A01C01T01, A01C01T02'
    assert lines[9] == '          town A01C01T02: Lyon'

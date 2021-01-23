# third party import
import pytest

import logging

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
def keys():
    keys = ['process', 'step', 'task']
    return keys


@pytest.fixture
def tree_datasets(keys):
    data = {'process':  ['X', 'Y', 'Y', 'Y', 'Z', 'Z'],
            'step': ['load data', 'load data', 'load data', 'aggregate', 'load data', 'aggregate', ],
            'task': ['read file', 'read file', 'parse file', 'average', 'read csv', 'sum']
            }

    df = pd.DataFrame(data, columns=keys)

    marks = "PST"
    dfs = extract_hierarchy(df, keys, marks)

    return dfs


# Tests
def test_build_tree(tree_datasets, logger, keys):
    tree = build_tree(tree_datasets, keys)

    assert tree
    assert len(tree['process_dict']) == 3
    p2 = tree['process_dict']['P02']
    assert len(p2['step_dict']) == 2
    p2s1 = p2['step_dict']['P02S01']
    assert len(p2s1['task_dict']) == 2
    p2s1t1 = p2s1['task_dict']['P02S01T01']
    assert p2s1t1['process'] == 'Y'
    assert p2s1t1['step'] == 'load data'
    assert p2s1t1['task'] == 'read file'


# Tests
def test_pretty_print_tree(tree_datasets, logger, keys):
    tree = build_tree(tree_datasets, keys)
    lines = pretty_print_tree(tree, keys)

    assert len(lines) == 32
    assert lines[0] == 'there are 3 process(s)'
    assert lines[1] == '  P01, P02, P03'
    assert lines[9] == '  process P02: Y'
    assert lines[10] == '    has 2 step(s)'
    assert lines[11] == '      P02S01, P02S02'
    assert lines[12] == '      step P02S01: load data'
    assert lines[13] == '        has 2 task(s)'
    assert lines[14] == '          P02S01T01, P02S01T02'
    assert lines[15] == '          task P02S01T01: read file'


# Tests
def test_build_tree_alt_names(logger):
    keys = ['repo', 'package', 'class']
    data = {'repo':  ['r1', 'r2', 'r2', 'r2', 'r3', 'r3'],
            'package': ['r1p1', 'r2p1', 'r2p1', 'r2p2', 'r3p1', 'r3p2', ],
            'class': ['r1p1c1', 'r2p1c1', 'r2p1c2', 'r2p2c1', 'r3p1c1', 'r3p2c1']
            }

    df = pd.DataFrame(data, columns=keys)

    marks = "RPC"

    dfs = extract_hierarchy(df, keys, marks)

    tree = build_tree(dfs, keys)

    assert tree
    assert len(tree['repo_dict']) == 3
    p2 = tree['repo_dict']['R02']
    assert len(p2['package_dict']) == 2
    p2s1 = p2['package_dict']['R02P01']
    assert len(p2s1['class_dict']) == 2
    p2s1t1 = p2s1['class_dict']['R02P01C01']
    assert p2s1t1['repo'] == 'r2'
    assert p2s1t1['package'] == 'r2p1'
    assert p2s1t1['class'] == 'r2p1c1'

    lines = pretty_print_tree(tree, keys)

    assert len(lines) == 32
    assert lines[0] == 'there are 3 repo(s)'
    assert lines[1] == '  R01, R02, R03'
    assert lines[9] == '  repo R02: r2'
    assert lines[10] == '    has 2 package(s)'
    assert lines[11] == '      R02P01, R02P02'
    assert lines[12] == '      package R02P01: r2p1'
    assert lines[13] == '        has 2 class(s)'
    assert lines[14] == '          R02P01C01, R02P01C02'
    assert lines[15] == '          class R02P01C01: r2p1c1'

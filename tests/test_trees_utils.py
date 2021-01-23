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

    df = pd.DataFrame(data, columns=['process', 'step', 'task'])

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

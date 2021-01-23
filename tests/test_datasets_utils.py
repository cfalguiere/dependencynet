# third party import
import pytest

import logging
import pandas as pd

# module import
from dependencynet.datasets_utils import extract_hierarchy


@pytest.fixture
def logger():
    logging.basicConfig()
    logger = logging.getLogger('test_datasets_utils')
    logger.setLevel(logging.WARN)


@pytest.fixture
def source_data():
    data = {'process':  ['X', 'Y', 'Y', 'Y', 'Z', 'Z'],
            'step': ['load data', 'load data', 'load data', 'aggregate', 'load data', 'aggregate', ],
            'task': ['read file', 'read file', 'parse file', 'average', 'read csv', 'sum']
            }

    df = pd.DataFrame(data, columns=['process', 'step', 'task'])

    return df


# Tests
def test_extract_hierarchy(source_data, logger):
    keys = ['process', 'step', 'task']
    marks = "PST"
    dfs = extract_hierarchy(source_data, keys, marks)

    assert len(dfs) == 3

    assert dfs[0].shape == (3, 4)
    assert dfs[0]['process'][1] == 'Y'
    assert dfs[0]['pos'][1] == 2
    assert dfs[0]['id'][1] == 'P02'
    assert dfs[0]['label'][1] == 'P02 Y'

    assert dfs[1].shape == (5, 6)
    assert dfs[1]['process'][2] == 'Y'
    assert dfs[1]['step'][2] == 'aggregate'
    assert dfs[1]['pos'][2] == 2
    assert dfs[1]['id_parent'][2] == 'P02'
    assert dfs[1]['id'][2] == 'P02S02'
    assert dfs[1]['label'][2] == 'P02S02 aggregate'

    assert dfs[2].shape == (6, 7)
    assert dfs[2]['process'][2] == 'Y'
    assert dfs[2]['step'][2] == 'load data'
    assert dfs[2]['task'][2] == 'parse file'
    assert dfs[2]['pos'][2] == 2
    assert dfs[2]['id_parent'][2] == 'P02S01'
    assert dfs[2]['id'][2] == 'P02S01T02'
    assert dfs[2]['label'][2] == 'P02S01T02 parse file'

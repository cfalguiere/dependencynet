"""
test fixtures
"""

# third party import
import pytest
from testfixtures import TempDirectory

import logging

from dependencynet.schema import SchemaBuilder


@pytest.fixture(autouse=True, scope="session")
def logger():
    logging.basicConfig()
    logger = logging.getLogger('test_datasets_utils')
    logger.setLevel(logging.DEBUG)


@pytest.fixture()
def root_location():
    with TempDirectory() as dir:
        yield dir


# ### Towns

# (scope="session")
@pytest.fixture
def schema_towns():
    schema = SchemaBuilder().level('area', 'A') \
                            .level('country', 'C') \
                            .level('town', 'T') \
                            .resource('monument', 'M', explode=True, delimiter=',') \
                            .render()
    return schema


@pytest.fixture(scope="session")
def compact_columns_towns():
    columns = ['area', 'country', 'town', 'monument']
    return columns


# ### Fanout

@pytest.fixture
def schema_fanout():
    schema = SchemaBuilder().level('L1', 'L1') \
                            .level('L2', 'L2') \
                            .level('L3', 'L3') \
                            .resource('RI', 'RI', role='INPUT', connect_id_name='R') \
                            .resource('RO', 'RO', role='OUTPUT', connect_id_name='R') \
                            .connect('RO', 'RI') \
                            .render()
    return schema


@pytest.fixture(scope="session")
def compact_columns_fanout():
    columns = ['L1', 'L2', 'L3', 'RO', 'RI']
    return columns

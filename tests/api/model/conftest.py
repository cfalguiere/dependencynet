"""
test fixtures
"""

# third party import
import pytest
from testfixtures import TempDirectory

import logging
from os import path
import pandas as pd

from dependencynet.schema import SchemaBuilder
from dependencynet.model import ModelBuilder


@pytest.fixture(autouse=True, scope="session")
def logger():
    logging.basicConfig()
    logger = logging.getLogger('test_datasets_utils')
    logger.setLevel(logging.DEBUG)


@pytest.fixture
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


@pytest.fixture
def compact_columns_towns():
    columns = ['area', 'country', 'town', 'monument']
    return columns


@pytest.fixture
def source_data_towns(schema_towns, compact_columns_towns):
    filename = path.join('tests', 'resources', 'data', 'compact', 'towns.csv')
    data = pd.read_csv(filename, delimiter=';')

    df = pd.DataFrame(data, columns=compact_columns_towns)
    return df


@pytest.fixture
def model_towns(source_data_towns, schema_towns):
    model = ModelBuilder().from_compact(source_data_towns) \
                          .with_schema(schema_towns) \
                          .render()
    return model

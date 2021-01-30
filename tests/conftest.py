"""
test fixtures
"""

# third party import
import pytest

import logging

from dependencynet.schema import SchemaBuilder


@pytest.fixture(autouse=True, scope="session")
def logger():
    logging.basicConfig()
    logger = logging.getLogger('test_datasets_utils')
    logger.setLevel(logging.WARN)


@pytest.fixture(scope="session")
def schema_towns():
    schema = SchemaBuilder().level('area', 'A') \
                            .level('country', 'C') \
                            .level('town', 'T') \
                            .render()
    return schema

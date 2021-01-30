# third party import
import pytest

import logging

# module import
from dependencynet.schema import SchemaBuilder


@pytest.fixture
def logger():
    logging.basicConfig()
    logger = logging.getLogger('test_datasets_utils')
    logger.setLevel(logging.WARN)


# Tests
def test_schema_builder_towns(logger):
    schema = SchemaBuilder().level('area', 'A') \
                            .level('country', 'C') \
                            .level('town', 'T') \
                            .resource('monument', 'M') \
                            .resource('station', 'S') \
                            .render()

    assert schema
    assert len(schema.levels['keys']) == 3
    assert len(schema.levels['marks']) == 3
    assert schema.levels['keys'][1] == 'country'
    assert schema.levels['marks'][1] == 'C'
    assert schema.resources['M'] == 'monument'

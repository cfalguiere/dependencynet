"""
This module tests base classes encoders
"""
# third party import
# import pytest


# module import
from dependencynet.core.datasource.encoders import SchemaEncoder


# Tests
def test_schema_encoder(schema_towns):
    encoded = SchemaEncoder().encode(schema_towns)

    assert 'levels' in encoded
    assert 'area' in encoded
    assert 'resources' in encoded

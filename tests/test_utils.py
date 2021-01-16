# test_dependencynet.py
# Tests for the dependencynet module

# standard import

# third party import
import pytest

# skoobpy import
from dependencynet.utils import dummy


@pytest.fixture
def dummy_helper():
    return 'dummy'


# Tests
def test_dummy(dummy_helper):
    result = dummy()
    assert dummy_helper == result

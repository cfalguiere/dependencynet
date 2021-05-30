"""
test fixtures
"""

# third party import
import pytest
from testfixtures import TempDirectory

import logging


@pytest.fixture(autouse=True, scope="session")
def logger():
    logging.basicConfig()
    logger = logging.getLogger('test_datasets_utils')
    logger.setLevel(logging.DEBUG)


@pytest.fixture
def root_location():
    with TempDirectory() as dir:
        yield dir

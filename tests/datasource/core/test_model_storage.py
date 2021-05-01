"""
This module tests the model storage features
"""
# third party import
import pytest

from os import path

import pandas as pd

# module import
from dependencynet.model import ModelBuilder
from dependencynet.datasource.core.modelstorage import ModelStorageService


@pytest.fixture
def source_data_towns(schema_towns, compact_columns_towns):
    filename = path.join('tests', 'resources', 'data', 'compact', 'towns.csv')
    data = pd.read_csv(filename, delimiter=';')

    df = pd.DataFrame(data, columns=compact_columns_towns)

    # FIXME factprize
    return df


# Tests
def test_model_storage_towns(source_data_towns, schema_towns, root_location):
    model = ModelBuilder().from_compact(source_data_towns) \
                          .with_schema(schema_towns) \
                          .render()
    assert model

    storage = ModelStorageService(root_location.path)
    storage.save(model)

    model_folder = path.join(root_location.path, 'current')

    assert path.exists(model_folder)
    assert path.isdir(model_folder)

    # schema
    schema_file = path.join(model_folder, 'schema.json')
    assert path.exists(schema_file)
    assert path.isfile(schema_file)

    # levels
    for name in schema_towns.levels_keys():
        level_dataset_file = path.join(model_folder, f'{name}.csv')
        assert path.exists(level_dataset_file)
        assert path.isfile(level_dataset_file)

    # resources
    if False:
        for name in schema_towns.resources_keys():
            resource_dataset_file = path.join(model_folder, f'{name}.csv')
            assert path.exists(resource_dataset_file)
            assert path.isfile(resource_dataset_file)

    # tree
    tree_file = path.join(model_folder, 'tree.json')
    assert path.exists(tree_file)
    assert path.isfile(tree_file)

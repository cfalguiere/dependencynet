"""
This module tests details of the resource loader
"""
# third party import
import pytest

from os import path
import pandas as pd

from dependencynet.datasource.loaders.levelsloader import LevelsLoader

# module import
from dependencynet.datasource.loaders.resourcesloader import ResourcesLoader


@pytest.fixture
def source_data_towns(schema_towns, compact_columns_towns):
    filename = path.join('tests', 'resources', 'data', 'compact', 'towns.csv')
    data = pd.read_csv(filename, delimiter=';')

    df = pd.DataFrame(data, columns=compact_columns_towns)

    # FIXME factprize
    return df


# Tests
def test_resources_loader_towns(source_data_towns, schema_towns):
    loader = LevelsLoader(schema_towns, source_data_towns)
    print(loader)
    levels_datasets = loader.extract_all()

    # towns
    parent_df = levels_datasets[2]

    loader = ResourcesLoader(schema_towns, source_data_towns, parent_df)
    resource_dfs = loader.extract_all()
    assert len(resource_dfs) == 1

    df_monument = resource_dfs['monument']
    assert df_monument.shape == (6, 8)
    assert list(df_monument.columns) == ['area', 'country', 'town', 'monument', 'pos', 'id_parent', 'id', 'label']


# Tests
def test_monument_loader_towns(source_data_towns, schema_towns):
    loader = LevelsLoader(schema_towns, source_data_towns)
    levels_datasets = loader.extract_all()

    # towns
    parent_df = levels_datasets[2]  # FIXME last item of list

    loader = ResourcesLoader(schema_towns, source_data_towns, parent_df)
    print(loader)
    df_monument = loader.extract(('monument'), '{id_parent}M{id:02d}')

    assert df_monument.shape == (6, 8)
    i_paris = 0
    assert list(df_monument.columns) == ['area', 'country', 'town', 'monument', 'pos', 'id_parent', 'id', 'label']
    assert df_monument['area'][i_paris] == 'Europe'
    assert df_monument['country'][i_paris] == 'France'
    assert df_monument['town'][i_paris] == 'Paris'
    assert df_monument['monument'][i_paris] == 'Eiffel Tower'  # FIXME
    assert df_monument['pos'][i_paris] == 1
    assert df_monument['id_parent'][i_paris] == 'A01C01T01'
    assert df_monument['id'][i_paris] == 'A01C01T01M01'
    assert df_monument['label'][i_paris] == 'A01C01T01M01 Eiffel Tower'

    # TODO tester lyon sans monument

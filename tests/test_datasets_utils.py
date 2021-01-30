# third party import
import pytest

from os import path
import pandas as pd


# module import
from dependencynet.datasets_utils import extract_hierarchy


@pytest.fixture
def source_data_towns(schema_towns):
    filename = path.join('tests', 'resources', 'data', 'compact', 'towns.csv')
    data = pd.read_csv(filename, delimiter=';')

    # TODO toutes les colonnes du csv
    df = pd.DataFrame(data, columns=schema_towns.levels_keys())

    return df


# Tests
def test_extract_hierarchy_towns(source_data_towns, schema_towns):
    dfs = extract_hierarchy(source_data_towns, schema_towns)

    assert len(dfs) == 3

    df_area = dfs[0]
    assert df_area.shape == (2, 4)
    assert list(df_area.columns) == ['area', 'pos', 'id', 'label']
    assert df_area['area'][4] == 'Asia'
    assert df_area['pos'][4] == 2
    assert df_area['id'][4] == 'A02'
    assert df_area['label'][4] == 'A02 Asia'

    df_country = dfs[1]
    assert df_country.shape == (4, 6)
    assert list(df_country.columns) == ['area', 'country', 'pos', 'id_parent', 'id', 'label']
    assert df_country['area'][2] == 'Europe'
    assert df_country['country'][2] == 'Italia'
    assert df_country['pos'][2] == 3
    assert df_country['id_parent'][2] == 'A01'
    assert df_country['id'][2] == 'A01C03'
    assert df_country['label'][2] == 'A01C03 Italia'

    df_town = dfs[2]
    print(df_town)
    assert df_town.shape == (5, 7)
    assert list(df_town.columns) == ['area', 'country', 'town', 'pos', 'id_parent', 'id', 'label']
    assert df_town['area'][1] == 'Europe'
    assert df_town['country'][1] == 'France'
    assert df_town['town'][1] == 'Lyon'
    assert df_town['pos'][1] == 2
    assert df_town['id_parent'][1] == 'A01C01'
    assert df_town['id'][1] == 'A01C01T02'
    assert df_town['label'][1] == 'A01C01T02 Lyon'

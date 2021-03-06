# third party import
import pytest

from os import path
import pandas as pd

# module import
from dependencynet.schema import SchemaBuilder
from dependencynet.model import ModelBuilder


@pytest.fixture
def source_data_towns(schema_towns, compact_columns_towns):
    filename = path.join('tests', 'resources', 'data', 'compact', 'towns.csv')
    data = pd.read_csv(filename, delimiter=';')

    df = pd.DataFrame(data, columns=compact_columns_towns)

    # FIXME factprize
    return df


@pytest.fixture
def wrong_schema():
    wrong_schema = SchemaBuilder().level('area', 'A') \
                            .level('country', 'C') \
                            .level('town', 'T') \
                            .resource('monument', 'M', explode=True, delimiter=',') \
                            .resource('doesnotexist', 'X') \
                            .render()
    return wrong_schema


# Tests
def test_model_builder_towns(source_data_towns, schema_towns):
    model = ModelBuilder().from_compact(source_data_towns) \
                          .with_schema(schema_towns) \
                          .render()

    assert model

    level_dfs = model.levels_datasets
    resource_dfs = model.resources_datasets

    assert len(level_dfs) == 3
    assert len(resource_dfs) == 1

    df_area = level_dfs[0]
    assert df_area.shape == (2, 4)
    assert list(df_area.columns) == ['area', 'pos', 'id', 'label']
    assert df_area['label'][4] == 'A02 Asia'

    df_country = level_dfs[1]
    assert df_country.shape == (4, 6)
    assert list(df_country.columns) == ['area', 'country', 'pos', 'id_parent', 'id', 'label']
    assert df_country['label'][2] == 'A01C03 Italia'

    df_town = level_dfs[2]
    assert df_town.shape == (5, 7)
    assert list(df_town.columns) == ['area', 'country', 'town', 'pos', 'id_parent', 'id', 'label']
    assert df_town['label'][1] == 'A01C01T02 Lyon'

    df_monument = resource_dfs['monument']
    assert df_monument.shape == (6, 8)
    i_paris = 0
    assert list(df_monument.columns) == ['area', 'country', 'town', 'monument', 'pos', 'id_parent', 'id', 'label']
    assert df_monument['label'][i_paris] == 'A01C01T01M01 Eiffel Tower'

    # TODO tester lyon sans monument


# Tests
def test_model_builder_field_not_found(source_data_towns, wrong_schema):
    with pytest.raises(RuntimeError) as excinfo:
        mb = ModelBuilder()
        mb.from_compact(source_data_towns).with_schema(wrong_schema).render()

    assert "doesnotexist not found in datasource" in str(excinfo.value)


# Tests
def test_model_builder_towns_has_schema(source_data_towns, schema_towns):
    model = ModelBuilder().from_compact(source_data_towns) \
                          .with_schema(schema_towns) \
                          .render()
    assert model
    assert model.schema


# Tests
def test_pretty_print(source_data_towns, schema_towns):
    model = ModelBuilder().from_compact(source_data_towns) \
                          .with_schema(schema_towns) \
                          .render()

    lines = model.pretty_print()

    assert len(lines) == 40
    assert lines[0] == 'there are 2 area(s)'
    assert lines[1] == '  A01, A02'
    assert lines[2] == '  area A01: Europe'
    assert lines[3] == '    has 3 country(s)'
    assert lines[4] == '      A01C01, A01C02, A01C03'
    assert lines[5] == '      country A01C01: France'
    assert lines[6] == '        has 2 town(s)'
    assert lines[7] == '          A01C01T01, A01C01T02'
    assert lines[8] == '          town A01C01T01: Paris'
    assert lines[9] == '            has 2 monument(s)'
    assert lines[10] == '               A01C01T01M01, A01C01T01M02'
    assert lines[11] == '                 monument A01C01T01M01: Eiffel Tower'
    assert lines[12] == '                 monument A01C01T01M02: Louvre Museum'
    assert lines[13] == '          town A01C01T02: Lyon'
    assert lines[14] == '            has 0 monument(s)'
    assert lines[15] == '      country A01C02: UK'


# TODO given model name

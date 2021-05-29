# third party import
import pytest

import re
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

    levels = ['area', 'country', 'town']

    def has_levels(df, n=3):
        return all(item in list(df.columns) for item in levels[0:n-1])

    def has_resources(df, keys):
        return all(item in list(df.columns) for item in keys)

    df_area = level_dfs[0]
    assert df_area.shape == (2, 4)
    assert has_levels(df_area, 1)
    labels = df_area['label'].tolist()
    assert 'A01 Europe' in labels
    assert 'A02 Asia' in labels

    df_country = level_dfs[1]
    assert df_country.shape == (4, 6)
    assert has_levels(df_country, 2)
    labels = df_country['label'].tolist()
    assert 'A01C01 France' in labels
    assert 'A01C02 UK' in labels
    assert 'A01C03 Italia' in labels
    assert 'A02C01 Japan' in labels

    df_town = level_dfs[2]
    assert df_town.shape == (5, 7)
    assert has_levels(df_town)
    labels = df_town['label'].tolist()
    assert 'A01C01T01 Paris' in labels
    assert 'A01C01T02 Lyon' in labels
    assert 'A01C02T01 London' in labels
    assert 'A01C03T01 Rome' in labels
    assert 'A02C01T01 Tokyo' in labels

    # WARNING order is not defined
    def select(s):
        return pattern.match(s)

    def extract_label(s):
        m = pattern.match(s)
        return m.group(1)

    df_monument = resource_dfs['monument']
    assert df_monument.shape == (6, 8)
    assert has_levels(df_monument)
    assert has_resources(df_monument, ['monument'])

    labels = df_monument['label'].tolist()
    pattern = re.compile(r"A\d{2}C\d{2}T\d{2}M\d{2} (.+)")
    selected = list(filter(pattern.match, labels))
    names = sorted([extract_label(s) for s in selected])
    assert names == sorted(['Eiffel Tower', 'Louvre Museum',
                            'Tower Bridge', 'Tower of London',
                            'Colosseum', 'Senso-ji'])


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

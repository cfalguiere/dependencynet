# third party import
import pytest

from os import path

import pandas as pd

# module import
from dependencynet.model import ModelBuilder
from dependencynet.tree_model import TreeModelBuilder


@pytest.fixture
def source_data_towns(schema_towns, compact_columns_towns):
    filename = path.join('tests', 'resources', 'data', 'compact', 'towns.csv')
    data = pd.read_csv(filename, delimiter=';')

    df = pd.DataFrame(data, columns=compact_columns_towns)

    # FIXME factprize
    return df


@pytest.fixture
def model_towns(source_data_towns, schema_towns):
    model = ModelBuilder().from_compact(source_data_towns) \
                          .with_schema(schema_towns) \
                          .render()
    return model


# Tests
def test_tree_model_towns(model_towns, schema_towns):
    # TODO resources
    tree_model = TreeModelBuilder().from_canonical(model_towns.levels_datasets, None) \
                             .with_schema(schema_towns) \
                             .render()
    tree = tree_model.tree

    assert tree
    assert len(tree['area_dict']) == 2
    a1 = tree['area_dict']['A01']
    assert len(a1['country_dict']) == 3
    a1c1 = a1['country_dict']['A01C01']
    assert len(a1c1['town_dict']) == 2
    a1c1t2 = a1c1['town_dict']['A01C01T02']
    assert a1c1t2['area'] == 'Europe'
    assert a1c1t2['country'] == 'France'
    assert a1c1t2['town'] == 'Lyon'


# Tests
def test_full_tree_model_towns(model_towns, schema_towns):
    # TODO resources
    tree_model = TreeModelBuilder().from_canonical(model_towns.levels_datasets,
                                                   model_towns.resources_datasets, ) \
                             .with_schema(schema_towns) \
                             .render()
    tree = tree_model.tree

    assert tree
    assert len(tree['area_dict']) == 2
    a1 = tree['area_dict']['A01']
    assert len(a1['country_dict']) == 3
    a1c1 = a1['country_dict']['A01C01']
    assert len(a1c1['town_dict']) == 2
    a1c1t2 = a1c1['town_dict']['A01C01T02']
    assert a1c1t2['area'] == 'Europe'
    assert a1c1t2['country'] == 'France'
    assert a1c1t2['town'] == 'Lyon'
    # Lyon does not have any monument
    assert 'monument_dict' not in a1c1t2['town']
    # FIXME tester lyon sans monument
    a1c1t1 = a1c1['town_dict']['A01C01T01']
    a1c1t1m1 = a1c1t1['monument_dict']['A01C01T01M01']
    assert a1c1t1m1['area'] == 'Europe'
    assert a1c1t1m1['country'] == 'France'
    assert a1c1t1m1['town'] == 'Paris'
    assert a1c1t1m1['monument'] == 'Eiffel Tower'

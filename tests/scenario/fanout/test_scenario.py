"""
Tests model creation using the dataset trips
TODO test viewer, graphml
TODO test test_graph_model all node and links level -> resource
"""
import pytest

# module import
from dependencynet.network.graphbuilder import GraphBuilder
from dependencynet.network.stylebuilder import StyleBuilder


@pytest.mark.fanout
def test_schema_builder(schema_fanout):
    a_schema = schema_fanout
    # .resource('station', 'S') \  # FIXME  fixture is altered ?

    assert a_schema
    assert len(a_schema.levels['keys']) == 3
    assert len(a_schema.levels['marks']) == 3
    assert a_schema.levels['keys'][0] == 'L1'
    assert a_schema.levels['marks'][0] == 'L1'
    assert a_schema.levels['keys'][1] == 'L2'
    assert a_schema.levels['marks'][1] == 'L2'
    assert a_schema.levels['keys'][2] == 'L3'
    assert a_schema.levels['marks'][2] == 'L3'
    assert a_schema.resources['RI']['mark'] == 'RI'
    assert a_schema.resources['RO']['mark'] == 'RO'

    # FIXME tests connect


@pytest.mark.fanout
def test_model_builder(model_fanout):
    model = model_fanout

    assert model

    level_dfs = model.levels_datasets
    resource_dfs = model.resources_datasets

    assert len(level_dfs) == 3
    assert len(resource_dfs) == 2

    levels = ['L1', 'L2', 'L3']

    def has_levels(df, n=3):
        return all(item in list(df.columns) for item in levels[0:n-1])

    def has_resources(df, keys):
        return all(item in list(df.columns) for item in keys)

    df_l1 = level_dfs[0]
    assert df_l1.shape == (4, 4)
    assert has_levels(df_l1, 1)
    labels = df_l1['label'].tolist()
    assert 'L101 REF' in labels
    assert 'L102 A' in labels
    assert 'L103 B' in labels
    assert 'L104 C' in labels

    df_l2 = level_dfs[1]
    assert df_l2.shape == (4, 6)
    assert has_levels(df_l2, 2)
    labels = df_l2['label'].tolist()
    assert 'L101L201 REF1' in labels
    assert 'L102L201 A1' in labels
    assert 'L103L201 B1' in labels
    assert 'L104L201 C1' in labels

    df_l3 = level_dfs[2]
    assert df_l3.shape == (4, 7)
    assert has_levels(df_l3)
    labels = df_l3['label'].tolist()
    assert 'L101L201L301 REF1a' in labels
    assert 'L102L201L301 A1a' in labels
    assert 'L103L201L301 B1a' in labels
    assert 'L104L201L301 C1a' in labels

    df_ri = resource_dfs['RI']
    assert df_ri.shape == (3, 9)
    assert has_levels(df_ri)
    assert has_resources(df_ri, ['RI', 'R'])
    labels = df_ri['label'].tolist()
    assert 'L102L201L301RI01 REF-out' in labels
    assert 'L103L201L301RI01 REF-out' in labels
    assert 'L104L201L301RI01 REF-out' in labels

    df_ro = resource_dfs['RO']
    assert df_ro.shape == (4, 9)
    assert has_levels(df_ro)
    assert has_resources(df_ro, ['RO', 'R'])
    labels = df_ro['label'].tolist()
    assert 'L101L201L301RO01 REF-out' in labels
    assert 'L102L201L301RO01 A-out' in labels
    assert 'L103L201L301RO01 B-out' in labels
    assert 'L104L201L301RO01 C-out' in labels


# Tests
@pytest.mark.fanout
def test_graph_model(class_mapping_fanout, model_fanout):
    graph_model = GraphBuilder().with_types(class_mapping_fanout).with_model(model_fanout).render()
    assert graph_model

    lines = graph_model.pretty_print()

    # assumes those have been tested by class test
    # nodes L1, L2, L3, RI, RO
    # edges L1 -> L2, L2 -> L3, L3 -> RI, L3 -> RO

    # check connectionx out -> in on flights
    pattern = 'RO output resource %s -> RI input resource %s'
    for pair in [('L101L201L301RO01', 'L102L201L301RI01'),
                 ('L101L201L301RO01', 'L103L201L301RI01'),
                 ('L101L201L301RO01', 'L104L201L301RI01')]:
        edge = pattern % pair
        assert edge in lines


@pytest.mark.fanout
def test_graphstyle(schema_fanout, compact_columns_fanout):
    sb = StyleBuilder(schema_fanout)
    graph_style = sb.render()

    selectors = [style['selector'] for style in graph_style]

    # check whether each node type is represented
    for element in compact_columns_fanout:
        selector = f'node.{element}'
        assert selector in selectors
        i = selectors.index(selector)
        assert 'background-color' in graph_style[i]['css']
        assert 'color' in graph_style[i]['css']

    # check connection
    connect_selector = 'node.R'
    assert connect_selector in selectors
    i = selectors.index(selector)
    assert 'background-color' in graph_style[i]['css']
    assert 'color' in graph_style[i]['css']

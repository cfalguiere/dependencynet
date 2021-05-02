"""
This module tests the graph model - test cases : connection one to many
"""
# third party import
import pytest

from os import path
import pandas as pd

from dependencynet.model import ModelBuilder

# module import
from dependencynet.network.graphbuilder import GraphBuilder, LevelNode
from dependencynet.network.graphbuilder import InputNode, OutputNode


@pytest.fixture
def source_data_fanout(schema_fanout, compact_columns_fanout):
    filename = path.join('tests', 'resources', 'data', 'compact', 'fanout.csv')
    data = pd.read_csv(filename, delimiter=';')

    df = pd.DataFrame(data, columns=compact_columns_fanout)
    return df


@pytest.fixture
def model_fanout(source_data_fanout, schema_fanout):
    model = ModelBuilder().from_compact(source_data_fanout) \
                          .with_schema(schema_fanout) \
                          .render()
    return model


class L1Node(LevelNode):
    def __init__(self, properties):
        super().__init__(properties, 'L1')


class L2Node(LevelNode):
    def __init__(self, properties):
        super().__init__(properties, 'L2')


class L3Node(LevelNode):
    def __init__(self, properties):
        super().__init__(properties, 'L3')


class RINode(InputNode):
    def __init__(self, properties):
        super().__init__(properties, 'RI', 'R')


class RONode(OutputNode):
    def __init__(self, properties):
        super().__init__(properties, 'RO', 'R')


@pytest.fixture
def class_mapping_fanout():
    return {'L1': L1Node, 'L2': L2Node, 'L3': L3Node,
            'RO': RONode, 'RI': RINode}


# Tests
def test_graph_model(class_mapping_fanout, model_fanout):
    graph_model = GraphBuilder().with_types(class_mapping_fanout).with_model(model_fanout).render()
    assert graph_model

    lines = graph_model.pretty_print()

    # check connectionx out -> in on flights
    assert len(lines) == 40
    for i in [37, 38, 39]:
        assert 'L101L201L301RO01' in lines[i]
        linkA = 'L102L201L301RI01' in lines[i]
        linkB = 'L103L201L301RI01' in lines[i]
        linkC = 'L104L201L301RI01' in lines[i]
        assert linkA or linkB or linkC

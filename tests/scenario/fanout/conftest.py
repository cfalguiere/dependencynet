"""
Fixtures for fanout
purpose : one node to many nodes
The dataset has
- 3 levels : L1, L2, L3
- 2 resources: RI, RO
- R in/out are connected
"""
import pytest
from os import path

import pandas as pd

# module import
from dependencynet.schema import SchemaBuilder
from dependencynet.model import ModelBuilder

from dependencynet.network.graphbuilder import LevelNode, InputNode, OutputNode


@pytest.fixture
def schema_fanout():
    schema = SchemaBuilder().level('L1', 'L1') \
                            .level('L2', 'L2') \
                            .level('L3', 'L3') \
                            .resource('RI', 'RI', role='INPUT', connect_id_name='R') \
                            .resource('RO', 'RO', role='OUTPUT', connect_id_name='R') \
                            .connect('RO', 'RI') \
                            .render()
    return schema


@pytest.fixture(scope="session")
def compact_columns_fanout():
    columns = ['L1', 'L2', 'L3', 'RO', 'RI']
    return columns


@pytest.fixture
def source_data_fanout(schema_fanout, compact_columns_fanout):
    filename = path.join('tests', 'scenario', 'fanout', 'resources', 'fanout.csv')
    data = pd.read_csv(filename, delimiter=';')

    df = pd.DataFrame(data, columns=compact_columns_fanout)
    return df


@pytest.fixture
def model_fanout(source_data_fanout, schema_fanout):
    model = ModelBuilder().from_compact(source_data_fanout) \
                          .with_schema(schema_fanout) \
                          .render()
    return model


@pytest.fixture
def class_mapping_fanout():
    return {'L1': L1Node, 'L2': L2Node, 'L3': L3Node,
            'RO': RONode, 'RI': RINode}


# networkx classes

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

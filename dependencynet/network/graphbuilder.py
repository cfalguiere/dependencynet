"""
This module provides helpers to setup the graph network
"""
import logging

import ipycytoscape
import networkx as nx


class CustomNode(ipycytoscape.Node):
    def __init__(self, id, label, classes):
        super().__init__()
        self.data['id'] = id
        self.data['label'] = label
        self.classes = classes


class LevelNode(CustomNode):
    def __init__(self, properties, category):
        super().__init__(properties['id'], properties['label'], f'{category} level')
        self.category = category


class ResourceNode(CustomNode):
    def __init__(self, properties, category):
        super().__init__(properties['id'], properties['label'], f'{category} resource')
        self.category = category


class InputNode(ResourceNode):
    def __init__(self, properties, category):
        super().__init__(properties, f'{category} input')
        self.category = category
        self.data['role_id'] = properties['role_id']


class OutputNode(ResourceNode):
    def __init__(self, properties, category):
        super().__init__(properties, f'{category} output')
        self.category = category
        self.data['role_id'] = properties['role_id']


class GraphModel():

    def __init__(self, G):
        self.G = G

    def copy(self):
        # TODO unit test
        return GraphModel(self.G.copy())


# TODO pattern builder
class GraphBuilder():
    logger = logging.getLogger(__name__)
    # TODO unit tests

    @classmethod
    def __init__(self):
        self.node_class = {}
        self.G = nx.DiGraph()

    @classmethod
    def with_types(self, node_class_mapping):
        self.node_class = node_class_mapping
        return self

    @classmethod
    def with_model(self, model):
        self.model = model
        return self

    @classmethod
    def render(self):
        self.logger.debug('render graph data')
        self.__build_from_schema()
        return GraphModel(self.G)

    #  basic operations

    @classmethod
    def __build_from_schema(self):
        self.logger.info('adding nodes from levels')
        self.add_nodes_from_levels()
        for key in self.model.schema.resources_keys():
            self.logger.info(f'adding resource nodes {key}')
            self.add_nodes_from_resource(key)
        for left, right in self.model.schema.connections_pairs():
            # FIXME no match - data id contains In or Out
            self.logger.info(f'adding connection {left} {right}')
            df = self.model.resource_dataset(right)
            self.add_edges_from(df, left, right,
                                on_target_key='role_id', on_source_key='role_id',
                                graph_key='role_id')

    @classmethod
    def register_node_type(self, category, class_name, color='black'):
        # FIXME unused color
        self.node_class[category] = class_name

    @classmethod
    def add_nodes_from_levels(self):
        keys = self.model.schema.levels_keys()
        dfs = self.model.levels_datasets
        nb = len(keys)

        self.logger.info('creating nodes for each level dataset')
        for i in range(0, nb):
            self.add_nodes_from(dfs[i], keys[i])

        self.logger.info('creating edges between levels')
        for i in range(1, nb):
            self.add_edges_from(dfs[i], keys[i-1], keys[i])

    @classmethod
    def add_nodes_from_resource(self, resource_key):
        keys = self.model.schema.levels_keys()
        df = self.model.resource_dataset(resource_key)

        self.logger.info(f'creating nodes for resource dataset {resource_key}')
        self.add_nodes_from(df, resource_key)

        self.logger.info('creating edges between lower level and resource')
        self.logger.debug(f'lower level {keys[-1]} resource_key {resource_key}')
        role = self.model.schema.resource_definition(resource_key)['role']
        self.logger.debug(f'role={role}')
        preceding = (role == 'INPUT')  # FIXME magic string
        # FIXME juste inverser le passage des parametres
        self.add_edges_from(df, keys[-1], resource_key, preceding=preceding)

    @classmethod
    def add_nodes_from(self, df, category):
        wf_records = df.to_dict('records')
        ctor = self.node_class.get(category)
        wf_nodes = [ctor(row) for row in wf_records]
        self.logger.debug(f'adding {len(wf_nodes)} as {category}')
        self.G.add_nodes_from(wf_nodes)

    @classmethod
    def add_edges_from(self, target_df, source_category, target_category,
                       preceding=False, graph_key='id',
                       on_source_key='id_parent', on_target_key='id'):
        source_nodes_by_id = {n.data[graph_key]: n for n in self.G.nodes() if source_category in n.classes}
        target_nodes_by_id = {n.data[graph_key]: n for n in self.G.nodes() if target_category in n.classes}
        self.logger.debug(f'preceding={preceding}')
        if preceding:
            edge_label = f'{target_category}_{source_category}'
        else:
            edge_label = f'{source_category}_{target_category}'
        self.logger.debug(f'edge_label={edge_label}')

        def add_edge(row):
            id_source = row[on_source_key]
            id_target = row[on_target_key]
            self.logger.debug(f'{id_source} -> {id_target}')
            self.logger.debug(f'{source_nodes_by_id[id_source]} -> {target_nodes_by_id[id_target]}')
            self.logger.debug(f'preceding={preceding}')
            if preceding:
                self.G.add_edge(target_nodes_by_id[id_target], source_nodes_by_id[id_source], label=edge_label)
            else:
                self.G.add_edge(source_nodes_by_id[id_source], target_nodes_by_id[id_target], label=edge_label)

        target_df.apply(add_edge, axis=1)

"""
This module provides helpers to setup the data model tree
"""
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class TreeModel:
    tree = None

    @classmethod
    def __init__(self, tree):
        self.tree = tree
        pass

    @classmethod
    def __repr__(self):
        return self.tree.__repr__()


class TreeModelBuilder():
    logger = logging.getLogger(__name__)

    @classmethod
    def __init__(self):
        pass

    @classmethod
    def from_canonical(self, levels_datasets, resources_datasets):
        self.levels_datasets = levels_datasets
        self.resources_datasets = resources_datasets
        return self

    @classmethod
    def with_schema(self, schema):
        logger.debug(f'with_schema {schema}')
        self.schema = schema
        return self

    @classmethod
    def render(self):
        levels_dfs = self.levels_datasets
        resources_dfs = self.resources_datasets
        keys = self.schema.levels_keys()
        tree = self.__build_tree(levels_dfs, keys, resources_dfs)
        return TreeModel(tree)

    # ---- private

    @classmethod
    def __add_resource(self, parent, res_name, groups):
        logger.debug(f'adding resource {res_name}')
        element_name = "%s_dict" % res_name
        parent[element_name] = {}
        for kr, vr in groups:
            records = vr.to_dict('records')
            parent[element_name][kr] = records[0]

    @classmethod
    def __add_resources(self, parent, parent_key):
        resources_dfs = self.resources_datasets
        if resources_dfs is not None:
            logger.debug(f'adding {len(resources_dfs)} resources for {parent_key}')
            for name, dfr in resources_dfs.items():
                mask_parent_key = dfr['id_parent'] == parent_key
                r = dfr[mask_parent_key].groupby('id')
                self.__add_resource(parent, name, r)

    @classmethod
    def __add_level(self, current_level, parent, parent_key):
        levels_dfs = self.levels_datasets
        max_level = len(levels_dfs) - 1
        keys = self.schema.levels_keys()

        logger.debug(f'adding level {current_level} parent key {parent_key}')

        element_name = "%s_dict" % keys[current_level]
        parent[element_name] = {}
        df = levels_dfs[current_level]
        if current_level == 0:
            level = levels_dfs[current_level].groupby('id')
        else:
            mask_parent_key = df['id_parent'] == parent_key
            level = df[mask_parent_key].groupby('id')
        for k, v in level:
            records = v.to_dict('records')
            parent[element_name][k] = records[0]

            if current_level < max_level:
                self.__add_level(current_level+1, parent[element_name][k], k)
            else:
                self.__add_resources(parent[element_name][k], k)

    @classmethod
    def __build_tree(self, levels_dfs, keys, resources_dfs):
        tree = defaultdict(dict)
        self.__add_level(0, tree, None)

        return tree

"""
This module provides helpers to setup the data model tree
"""
import logging
from collections import defaultdict
from json import JSONEncoder

logger = logging.getLogger(__name__)


class TreeModel:
    tree = None

    @classmethod
    def __init__(self, tree):
        self.tree = tree
        pass

    @classmethod
    def __repr__(self):
        return "<TreeModel>"


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
        self.schema = schema
        return self

    @classmethod
    def render(self):
        dfs = self.levels_datasets
        keys = self.schema.levels_keys()
        tree = self.__build_tree(dfs, keys)
        return TreeModel(tree)

    # ---- private

    @classmethod
    def __build_tree(self, dfs, keys):
        tree = defaultdict(dict)
        elt0_name = "%s_dict" % keys[0]
        tree[elt0_name]

        l0 = dfs[0].groupby('id')
        for k0, v0 in l0:
            records = v0.to_dict('records')
            tree[elt0_name][k0] = records[0]
            elt1_name = "%s_dict" % keys[1]
            tree[elt0_name][k0][elt1_name] = {}

            df1 = dfs[1]
            l1 = df1[df1['id_parent'] == k0].groupby('id')
            for k1, v1 in l1:
                records = v1.to_dict('records')
                tree[elt0_name][k0][elt1_name][k1] = records[0]
                elt2_name = "%s_dict" % keys[2]
                tree[elt0_name][k0][elt1_name][k1][elt2_name] = {}

                df2 = dfs[2]
                l2 = df2[df2['id_parent'] == k1].groupby('id')
                for k2, v2 in l2:
                    records = v2.to_dict('records')
                    tree[elt0_name][k0][elt1_name][k1][elt2_name][k2] = records[0]

        return tree


class TreeModelEncoder(JSONEncoder):
    def default(self, o):
        return o.tree

    # def from_json(json_object):
    #    if 'fname' in json_object:
    #       return FileItem(json_object['fname'])
    # f = JSONDecoder(object_hook = from_json).decode('{"fname": "/foo/bar"}')

"""
This module provides helpers to setup the data model
"""
from os import path, makedirs
import logging
import json

from dependencynet.schema import SchemaEncoder
from dependencynet.tree_model import TreeModelBuilder, TreeModelEncoder
from dependencynet.datasource.loaders.resourcesloader import ResourcesLoader
from dependencynet.datasource.loaders.levelsloader import LevelsLoader


class Model:

    @classmethod
    def __init__(self, schema, levels_datasets, resources_datasets, tree_model):
        self.schema = schema
        self.levels_datasets = levels_datasets  # list
        self.resources_datasets = resources_datasets   # map
        self.tree_model = tree_model

    @classmethod
    def __repr__(self):
        nbl = len(self.levels_datasets)
        nbr = len(self.resources_datasets)
        return f"<Model levels_datasets {nbl} resources_datasets {nbr}>"

    @property
    def schema(self):
        return self.schema

    @property
    def levels_datasets(self):
        return self.levels_datasets

    @property
    def resources_datasets(self):
        return self.resources_datasets

    @property
    def tree_model(self):
        return self.tree_model

    @classmethod
    def level_dataset(self, pos):
        # TODO check for quality
        return self.levels_datasets[pos]  # pos is an int

    @classmethod
    def resource_dataset(self, key):
        # TODO check for quality
        return self.resources_datasets[key]  # jey is a string

    @classmethod
    def pretty_print(self):
        tree = self.tree_model.tree
        keys = self.schema.levels_keys()
        resources_keys = self.schema.resources_keys()

        lines = []
        elt0_name = "%s_dict" % keys[0]
        l0 = tree[elt0_name]
        lines.append(f"there are {len(l0)} {keys[0]}(s)")
        lines.append(f"  {', '.join([str(p) for p in [*l0]])}")

        for k0, v0 in l0.items():
            lines.append(f"  {keys[0]} {k0}: {v0[keys[0]]}")
            elt1_name = "%s_dict" % keys[1]
            l1 = v0[elt1_name]
            lines.append(f"    has {len(l1)} {keys[1]}(s)")
            lines.append(f"      {', '.join([str(i) for i in [*l1]])}")

            for k1, v1 in l1.items():
                lines.append(f"      {keys[1]} {k1}: {v1[keys[1]]}")
                elt2_name = "%s_dict" % keys[2]
                l2 = v1[elt2_name]
                lines.append(f"        has {len(l2)} {keys[2]}(s)")
                lines.append(f"          {', '.join([str(i) for i in [*l2]])}")
                for k2, v2 in l2.items():
                    lines.append(f"          {keys[2]} {k2}: {v2[keys[2]]}")

                    for name in resources_keys:
                        eltr_name = "%s_dict" % name
                        lr = v2[eltr_name]
                        lines.append(f"            has {len(lr)} {name}(s)")
                        if len(lr) > 0:
                            lines.append(f"               {', '.join([str(i) for i in [*lr]])}")
                            for kr, vr in lr.items():
                                lines.append(f"                 {name} {kr}: {vr[name]}")

        return lines


class ModelBuilder():
    logger = logging.getLogger(__name__)

    @classmethod
    def __init__(self):
        self.source_df = None
        self.schema = None

    @classmethod
    def from_compact(self, source_df):
        # TODI check whether mark is unique
        # TODO which is key
        self.source_df = source_df
        return self

    @classmethod
    def with_schema(self, schema):
        self.schema = schema
        return self

    @classmethod
    def render(self):
        self.logger.debug('render getting levels')
        loader = LevelsLoader(self.schema, self.source_df)
        levels_datasets = loader.extract_all()

        df_parent = levels_datasets[2]  # FIXME last item of list

        self.logger.debug('render getting datasets')
        loader = ResourcesLoader(self.schema, self.source_df, df_parent)
        resources_datasets = loader.extract_all()

        self.logger.debug('render building tree model')
        tree_model = TreeModelBuilder().from_canonical(levels_datasets, resources_datasets) \
                                       .with_schema(self.schema) \
                                       .render()

        self.logger.debug('render creating resulting model')

        return Model(self.schema, levels_datasets, resources_datasets, tree_model)


class ModelStorageService:
    logger = logging.getLogger(__name__)

    @classmethod
    def __init__(self, root_location, sep=','):
        self.root_location = root_location
        self.sep = sep

    @classmethod
    def load(self, schema, filename, sep=','):
        # TODO
        pass

    @classmethod
    def save(self, model, model_name='current'):
        try:
            makedirs(self.root_location, exist_ok=True)
            model_folder = path.join(self.root_location, model_name)
            makedirs(model_folder, exist_ok=True)  # TODO clean before replace
            self.logger.info("model folder is %s", model_folder)
            self.__save_schema(model_folder, model)
            self.__save_levels(model_folder, model)
            self.__save_resources(model_folder, model)
            self.__save_tree(model_folder, model)
        except Exception as err:
            self.logger.error('Model not saved. Reason: %s', err)

    # ---- private

    @classmethod
    def __save_schema(self, model_folder, model):
        self.logger.debug("__save_schema")
        filename = path.join(model_folder, 'schema.json')
        with open(filename, "w") as fh:
            json.dump(model.schema, fh, cls=SchemaEncoder, indent=2)
            self.logger.info("schema saved under name %s", filename)

    @classmethod
    def __save_levels(self, model_folder, model):
        names = model.schema.levels_keys()
        self.logger.debug(f"__save_levels names={names}")

        def save_level(df, name):
            self.logger.debug(f"save_level {name}")
            filename = path.join(model_folder, f'{name}.csv')
            df.to_csv(filename, sep=self.sep, index=False)
            self.logger.info("dateset saved under name %s", filename)

        [save_level(model.levels_datasets[i], names[i]) for i in range(len(names))]

    @classmethod
    def __save_resources(self, model_folder, model):
        names = model.schema.resources_keys()
        self.logger.debug(f"__save_resources names={names}")

        def save_resource(df, name):
            self.logger.debug(f"save_resource {name}")
            filename = path.join(model_folder, f'{name}.csv')
            df.to_csv(filename, sep=self.sep, index=False)
            self.logger.info("dateset saved under name %s", filename)

        [save_resource(model.resource_dataset(name), name) for name in names]

    @classmethod
    def __save_tree(self, model_folder, model):
        filename = path.join(model_folder, 'tree.json')
        with open(filename, "w") as fh:
            json.dump(model.tree_model, fh, cls=TreeModelEncoder, indent=2)
            self.logger.info("tree saved under name %s", filename)

"""
This module provides helpers to setup the data model
"""
import logging

from dependencynet.core.model.tree_model import TreeModelBuilder
from dependencynet.core.datasource.resourcesloader import ResourcesLoader
from dependencynet.core.datasource.levelsloader import LevelsLoader
from dependencynet.core.datasource.modelstorage import ModelStorageService
from dependencynet.core.datasource.modelprettyprinter import ModelPrettyPrinter


class Model:

    @classmethod
    def __init__(self, schema, levels_datasets, resources_datasets, tree_model):
        self.schema = schema
        self.levels_datasets = levels_datasets  # list
        self.resources_datasets = resources_datasets   # map
        self.tree_model = tree_model
        self.is_empty = self.tree_model is None

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
        service = ModelPrettyPrinter(self.tree_model, self.schema)
        return service.pretty_print()

    @classmethod
    def save(self, folder_name):
        # TODO unit test
        storage = ModelStorageService(folder_name)
        storage.save(self)


class EmptyModel(Model):
    @classmethod
    def __init__(self, schema):
        super().__init__(schema, None, None, None)

    @classmethod
    def __repr__(self):
        return "<EmptyModel>"

    @property
    def schema(self):
        return self.schema


class ModelBuilder():
    logger = logging.getLogger(__name__)

    @classmethod
    def __init__(self):
        self.source_df = None
        self.schema = None
        self.is_empty = True

    @classmethod
    def from_compact(self, source_df):
        # TODI check whether mark is unique
        # TODO which is key
        self.source_df = source_df
        self.is_empty = False
        return self

    @classmethod
    def with_schema(self, schema):
        self.schema = schema
        return self

    @classmethod
    def render(self):
        if self.is_empty:
            return EmptyModel(self.schema)
        else:
            return self.__render_model()

    @classmethod
    def __render_model(self):
        self.logger.debug('render getting levels')
        loader = LevelsLoader(self.schema, self.source_df)
        levels_datasets = loader.extract_all()

        df_parent = levels_datasets[-1]

        self.logger.debug('render getting datasets')
        loader = ResourcesLoader(self.schema, self.source_df, df_parent)
        resources_datasets = loader.extract_all()

        self.logger.debug('render building tree model')
        tree_model = TreeModelBuilder().from_canonical(levels_datasets, resources_datasets) \
                                       .with_schema(self.schema) \
                                       .render()

        self.logger.debug('render creating resulting model')

        return Model(self.schema, levels_datasets, resources_datasets, tree_model)

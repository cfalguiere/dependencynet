"""
This module provides helpers to setup the data model
"""
from os import path, makedirs
import logging
import json

import pandas as pd

from dependencynet.schema import SchemaEncoder

logger = logging.getLogger(__name__)


class Model:
    levels_datasets = None
    schema = None

    @classmethod
    def __init__(self, schema, levels_datasets):
        self.schema = schema
        self.levels_datasets = levels_datasets

    @classmethod
    def __repr__(self):
        return f"<Model levels_datasets {len(self.levels_datasets)}>"

    @classmethod
    def level_dataset(self, pos):
        # TODO check for quality
        return self.levels_datasets[pos]


class ModelBuilder():
    logger = logging.getLogger(__name__)

    @classmethod
    def __init__(self):
        pass

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
        levels_datasets = self.__extract_hierarchy(self.source_df, self.schema)
        return Model(self.schema, levels_datasets)

    # ---- private

    @classmethod
    def __extract_items_root(self, df, keys, id_pattern):
        logger.debug('extract_items_root keys=%s id_pattern=%s', keys, id_pattern)

        id_key = keys[-1]
        pos_key = 'pos'
        logger.debug('extract_items_root id_key=%s', id_key)

        items_df = df.drop_duplicates(subset=keys)[keys]

        def get_pos():
            i = 0
            while i < len(items_df.index):
                yield i
                i += 1

        items_df[pos_key] = pd.DataFrame(list(get_pos()), index=items_df.index)
        items_df[pos_key] = items_df[pos_key] + 1

        def format_id(p):
            id = id_pattern.format(id=p)
            return id

        items_df['id'] = items_df[pos_key].apply(lambda x: format_id(x))
        items_df['label'] = items_df.apply(lambda row: "%s %s" % (row['id'], row[id_key]), axis=1)

        logger.info('extract_items_root keys=%s id_pattern=%s => shape=%s', keys, id_pattern, items_df.shape)

        return items_df

    @classmethod
    def __extract_items_non_root(self, df, keys, id_pattern, parent_df):
        logger.debug('extract_items_non_root keys=%s id_pattern=%s', keys, id_pattern)

        id_key = keys[-1]
        parent_keys = keys[0:-1]
        logger.debug('extract_items_non_root id_key=%s', id_key)

        pos_key = 'pos'

        items_df = df.drop_duplicates(subset=keys)[keys]

        items_df[pos_key] = items_df.groupby(parent_keys).cumcount()
        items_df[pos_key] = items_df[pos_key] + 1

        # enrich with parent id
        items_df = pd.merge(items_df, parent_df[parent_keys + ['id']], on=parent_keys)
        columns_mapping = {
            'id': 'id_parent'
        }
        items_df = items_df.rename(columns=columns_mapping)

        items_df['id'] = items_df.apply(
                    lambda row: id_pattern.format(id=row[pos_key], id_parent=row['id_parent']),
                    axis=1)
        items_df['label'] = items_df.apply(lambda row: "%s %s" % (row['id'], row[id_key]), axis=1)

        logger.info('extract_items_root keys=%s id_pattern=%s => shape=%s', keys, id_pattern, items_df.shape)

        return items_df

    @classmethod
    def __extract_hierarchy(self, df, schema):
        dfs = []
        logger.debug('extract_hierarchy schema=%s', schema)

        keys = schema.levels_keys()
        marks = schema.levels_marks()

        pattern = '%s{id:02d}' % marks[0]

        df_parent = self.__extract_items_root(df, [keys[0]], pattern)
        dfs.append(df_parent)
        for i in range(1, len(keys)):
            df_i = self.__extract_items_non_root(df, keys[0:i+1], '{id_parent}%s{id:02d}' % marks[i], df_parent)
            dfs.append(df_i)
            df_parent = df_i
        return dfs


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
            logger.info("model folder is %s", model_folder)
            self.__save_schema(model_folder, model)
            self.__save_levels(model_folder, model)
        except Exception as err:
            logger.error('Model not saved. Reason: %s', err)

    # ---- private

    @classmethod
    def __save_schema(self, model_folder, model):
        filename = path.join(model_folder, 'schema.json')
        with open(filename, "w") as fh:
            json.dump(model.schema, fh, cls=SchemaEncoder, indent=2)
            logger.info("schema saved under name %s", filename)

    @classmethod
    def __save_levels(self, model_folder, model):
        names = model.schema.levels_keys()

        def save_level(df, name):
            filename = path.join(model_folder, f'{name}.csv')
            df.to_csv(filename, sep=self.sep, index=False)
            logger.info("dateset saved under name %s", filename)

        [save_level(model.levels_datasets[i], names[i]) for i in range(len(names))]

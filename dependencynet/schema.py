"""
This module provides helpers to manage the data schema
"""
import logging


class SchemaOperations:
    logger = logging.getLogger(__name__)

    @staticmethod
    def load(self, schema, filename, sep=','):
        # TODO
        pass

    @staticmethod
    def save(self, schema, filename, sep=','):
        # TODO
        pass


class SchemaBuilder:
    logger = logging.getLogger(__name__)

    @classmethod
    def __init__(self):
        self.levels = {'keys': [], 'marks': []}  # must keep order
        self.resources = {}

    @classmethod
    def level(self, label, mark):
        # TODI check whether mark is unique
        self.levels['keys'].append(label)
        self.levels['marks'].append(mark)
        return self

    @classmethod
    def resource(self, label, mark):
        # TODI check whether mark is unique
        # TODO which is key
        self.resources[mark] = label
        return self

    @classmethod
    def render(self):
        self.logger.info("rendering schema")
        return Schema(self.levels, self.resources)


class Schema:
    levels = None
    resources = None

    # TODO level resource info

    @classmethod
    def __init__(self, levels, resources):
        self.levels = levels
        self.resources = resources

    @classmethod
    def __repr__(self):
        return f"<Schema levels {self.levels} - resources {self.resources}>"

    @classmethod
    def levels_keys(self):
        return self.levels['keys']

    @classmethod
    def levels_marks(self):
        return self.levels['marks']

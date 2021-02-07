"""
This module provides helpers to manage the data schema
"""
import logging
from json import JSONEncoder


class Schema:

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

    @classmethod
    def resources_keys(self):
        return list(self.resources.keys())

    @classmethod
    def resource_mark(self, key):
        return self.resources[key]['mark']

    @classmethod
    def resource_definition(self, key):
        return self.resources[key]


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
    def resource(self, label, mark, explode=False, delimiter='|'):
        # TODI check whether mark is unique
        # TODO which is key
        self.resources[label] = {'mark': mark, 'explode': explode, 'delimiter': delimiter}
        return self

    @classmethod
    def render(self):
        self.logger.info("rendering schema")
        return Schema(self.levels, self.resources)


class SchemaStorage:
    logger = logging.getLogger(__name__)

    @staticmethod
    def load(self, schema, filename, sep=','):
        # TODO
        pass

    @staticmethod
    def save(self, schema, filename, sep=','):
        # TODO
        pass


class SchemaEncoder(JSONEncoder):
    def default(self, o):
        properties = {'levels': o.levels, 'resources': o.resources}
        return properties

    # def from_json(json_object):
    #    if 'fname' in json_object:
    #       return FileItem(json_object['fname'])
    # f = JSONDecoder(object_hook = from_json).decode('{"fname": "/foo/bar"}')

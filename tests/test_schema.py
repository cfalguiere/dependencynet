# third party import

# module import
from dependencynet.schema import SchemaBuilder

# TODO Schema SchemaOperations


# Tests
def test_schema_builder_towns():
    schema = SchemaBuilder().level('area', 'A') \
                            .level('country', 'C') \
                            .level('town', 'T') \
                            .resource('monument', 'M') \
                            .resource('station', 'S') \
                            .render()

    assert schema
    assert len(schema.levels['keys']) == 3
    assert len(schema.levels['marks']) == 3
    assert schema.levels['keys'][1] == 'country'
    assert schema.levels['marks'][1] == 'C'
    assert schema.resources['M'] == 'monument'


# Tests
def test_schema_level_keys_towns(schema_towns):
    keys = schema_towns.levels_keys()

    assert keys == ['area', 'country', 'town']


# Tests
def test_schema_level_marks_towns(schema_towns):
    keys = schema_towns.levels_marks()

    assert keys == ['A', 'C', 'T']

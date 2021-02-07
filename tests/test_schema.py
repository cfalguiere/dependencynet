# third party import

# module import
from dependencynet.schema import SchemaBuilder, SchemaEncoder

# TODO Schema SchemaOperations


# Tests
def test_schema_builder_towns():
    a_schema = SchemaBuilder().level('area', 'A') \
                            .level('country', 'C') \
                            .level('town', 'T') \
                            .resource('monument', 'M') \
                            .render()
    # .resource('station', 'S') \  # FIXME  fixture is altered ?

    assert a_schema
    assert len(a_schema.levels['keys']) == 3
    assert len(a_schema.levels['marks']) == 3
    assert a_schema.levels['keys'][1] == 'country'
    assert a_schema.levels['marks'][1] == 'C'
    assert a_schema.resources['monument']['mark'] == 'M'
    assert a_schema.resources['monument']['explode'] is False


# Tests
def test_schema_builder_explode_towns():
    a_schema = SchemaBuilder().level('area', 'A') \
                            .level('country', 'C') \
                            .level('town', 'T') \
                            .resource('monument', 'M', explode=True, delimiter=',') \
                            .render()

    assert a_schema.resources['monument']['explode'] is True
    assert a_schema.resources['monument']['delimiter'] == ','


# Tests
def test_schema_level_keys_towns(schema_towns):
    keys = schema_towns.levels_keys()

    assert keys == ['area', 'country', 'town']


# Tests
def test_schema_level_marks_towns(schema_towns):
    marks = schema_towns.levels_marks()

    assert marks == ['A', 'C', 'T']


# Tests
def test_schema_resource_keys_towns(schema_towns):
    keys = schema_towns.resources_keys()

    assert keys == ['monument']


# Tests
def test_schema_resource_mark_towns(schema_towns):
    mark = schema_towns.resource_mark('monument')

    assert mark == 'M'


# Tests
def test_schema_resource_definition_towns(schema_towns):
    definition = schema_towns.resource_definition('monument')
    assert definition['explode'] is True
    assert definition['delimiter'] == ','


# Tests
def test_schema_encoder(schema_towns):
    encoded = SchemaEncoder().encode(schema_towns)

    assert 'levels' in encoded
    assert 'area' in encoded
    assert 'resources' in encoded

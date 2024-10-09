import pytest

from jsonschema_schema_validator import exceptions
from jsonschema_schema_validator import validator


@pytest.mark.parametrize(
    'schema',
    [
        {'exclusiveMaximum': 99},
        {'exclusiveMinimum': 0},
        {'maximum': 99},
        {'minimum': 0},
        {'multipleOf': 1},
    ],
)
def test_valid(schema):
    schema = {'type': 'integer', **schema}
    validator._validate_integer(schema)


@pytest.mark.parametrize(
    'schema',
    [
        {'exclusiveMaximum': 'a string'},
        {'exclusiveMinimum': 'a string'},
        {'maximum': 'a string'},
        {'minimum': 'a string'},
        {'multipleOf': 'a string'},
        {'multipleOf': -2},
        {'minimummmmm': 123},
    ],
)
def test_invalid(schema):
    schema = {'type': 'integer', **schema}
    with pytest.raises(exceptions.ValidationError):
        validator._validate_integer(schema)


def test_invalid_type():
    schema = {'type': 'boolean'}
    with pytest.raises(RuntimeError) as exc:
        validator._validate_integer(schema)
    assert "'type' must be 'integer'" in str(exc)

import pytest
import uuid
from src.csv_schema.core.models import ConfigProperty, BaseConfigObject


def test_it_defaults_the_value():
    prop = ConfigProperty('a', default=None)
    assert prop.value is None

    prop = ConfigProperty('a', default='b')
    assert prop.value == 'b'

    prop = ConfigProperty('a')
    assert prop.value is None

    prop = ConfigProperty('a', default=BaseConfigObject)
    assert isinstance(prop.value, BaseConfigObject)


def test_clear():
    # Values
    for default in ['', None, 1, True, False, BaseConfigObject()]:
        prop = ConfigProperty('prop-name', str(uuid.uuid4()), '', default=default)
        assert prop.value != default
        prop.clear()
        assert prop.value == default

    # Types
    for default in [str, BaseConfigObject]:
        prop = ConfigProperty('prop-name', str(uuid.uuid4()), '', default=default)
        assert prop.value != default
        prop.clear()
        assert isinstance(prop.value, default)
        assert prop.value != default

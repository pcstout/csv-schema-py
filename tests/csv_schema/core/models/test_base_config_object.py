import pytest
import json
import uuid
from src.csv_schema.core.models import BaseConfigObject, ConfigProperty

class TestConfigChildChild(BaseConfigObject):
    __test__ = False
    def __init__(self):
        super(TestConfigChildChild, self).__init__()
        self.prop_cca = self.register_property(ConfigProperty('prop_cca'))
        self.prop_ccb = self.register_property(ConfigProperty('prop_ccb'))

    def on_validate(self):
        errors = []
        if self.prop_cca.value != 'prop_cca':
            errors.append('prop_cca value should be: "prop_cca"')
        return errors


class TestConfigChild(BaseConfigObject):
    __test__ = False
    def __init__(self):
        super(TestConfigChild, self).__init__()
        self.prop_ca = self.register_property(ConfigProperty('prop_ca'))
        self.prop_cb = self.register_property(ConfigProperty('prop_cb', default=TestConfigChildChild))


class TestConfig(BaseConfigObject):
    __test__ = False
    def __init__(self):
        super(TestConfig, self).__init__()
        self.prop_a = self.register_property(ConfigProperty('prop_a'))
        self.prop_b = self.register_property(ConfigProperty('prop_b'))
        self.prop_c = self.register_property(ConfigProperty('prop_c', default=TestConfigChild))
        self.prop_d = self.register_property(ConfigProperty('prop_d', default=list))
        self.prop_d.value.append(TestConfigChild())

    def on_validate(self):
        errors = []
        if self.prop_a.value != 'prop_a':
            errors.append('prop_a value should be: "prop_a"')
        return errors


def assert_not_default(props):
    """Asserts that all properties in the property hierarchy are not set to the default value."""
    for prop in props:
        if isinstance(prop.value, BaseConfigObject):
            assert_not_default(prop.value.properties)
        else:
            assert prop.value != prop.default


def assert_are_default(props):
    """Asserts that all properties in the property hierarchy are not set to the default value."""
    for prop in props:
        if isinstance(prop.value, BaseConfigObject):
            assert isinstance(prop.value, prop.default)
            assert_are_default(prop.value.properties)
        elif isinstance(prop.default, type):
            assert prop.value != prop.default
            assert isinstance(prop.value, prop.default)
        else:
            assert prop.value == prop.default


def populate_props(obj):
    """Populates all the property values in the property hierarchy."""
    for prop in obj.properties:
        if isinstance(prop.value, BaseConfigObject):
            populate_props(prop.value)
        else:
            prop.value = str(uuid.uuid4())


@pytest.fixture
def test_config():
    config = TestConfig()
    populate_props(config)
    return config


def test_register_property():
    config_obj = BaseConfigObject()
    prop = ConfigProperty('test')

    # Adds it and returns it.
    assert config_obj.register_property(prop) == prop
    assert prop in config_obj.properties

    # Does not duplicate it.
    config_obj.register_property(prop)
    assert prop in config_obj.properties
    assert len(config_obj.properties) == 1


def test_clear(test_config):
    assert_not_default(test_config.properties)
    test_config.clear()
    assert_are_default(test_config.properties)


def test_to_dict(test_config):
    d = test_config.to_dict()
    assert len(d) == len(test_config.properties)

    def assert_check(props, _dict):
        for prop in props:
            if isinstance(prop.value, BaseConfigObject):
                child_d = prop.value.to_dict()
                assert _dict[prop.name] == child_d
                assert_check(prop.value.properties, child_d)
            else:
                assert _dict[prop.name] == prop.value

    assert_check(test_config.properties, d)


def test_to_json(test_config):
    d = test_config.to_dict()
    j = test_config.to_json()
    assert json.loads(j) == d


def test_from_json(test_config):
    j = test_config.to_json()
    test_config.clear()
    test_config.from_json(j)
    assert test_config.to_json() == j


def test_to_md_help(test_config):
    # TODO: How to test this?
    print(test_config.to_md_help())


def test_is_valid(test_config):
    assert test_config.is_valid() is False
    test_config.prop_a.value = 'prop_a'
    test_config.prop_c.value.prop_cb.value.prop_cca.value = 'prop_cca'
    assert test_config.is_valid() is True


def test_validate(test_config):
    errors = test_config.validate()
    assert len(errors) == 2
    assert errors[0] == 'prop_a value should be: "prop_a"'
    assert errors[1] == '"prop_c" -> "prop_cb" -> prop_cca value should be: "prop_cca"'
    test_config.prop_a.value = 'prop_a'
    test_config.prop_c.value.prop_cb.value.prop_cca.value = 'prop_cca'
    errors = test_config.validate()
    assert len(errors) == 0

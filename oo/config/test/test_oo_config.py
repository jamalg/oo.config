import os

import pytest

from oo.config import OOConfig, EnvironmentVariable, IntEnvironmentVariable, \
    BoolEnvironmentVariable, FloatEnvironmentVariable


def test_simple_environment_variable():
    class TestConfig(OOConfig):
        # Test regular usage
        VAR = EnvironmentVariable("VAR_0")
        # Test without variable name
        VAR_1 = EnvironmentVariable()
        # Test default
        VAR_2 = EnvironmentVariable("VAR_2", default=1)
        VAR_3 = EnvironmentVariable("VAR_3", default=1)

    os.environ["VAR_0"] = "VALUE_0"
    os.environ["VAR_1"] = "VALUE_1"
    os.environ["VAR_3"] = "VALUE_3"

    test_config = TestConfig()
    assert test_config.VAR == "VALUE_0"
    assert test_config.VAR_1 == "VALUE_1"
    assert test_config.VAR_2 == 1
    assert test_config.VAR_3 == "VALUE_3"


def test_raises_if_no_value_nor_default():
    class TestConfig(OOConfig):
        VAR = EnvironmentVariable()

    with pytest.raises(ValueError):
        TestConfig()


def test_int_environment_variable():
    class TestConfig(OOConfig):
        VAR = IntEnvironmentVariable()

    os.environ["VAR"] = "1"

    test_config = TestConfig()
    assert test_config.VAR == 1


def test_bad_int_environment_variable():
    class TestConfig(OOConfig):
        VAR = IntEnvironmentVariable()

    os.environ["VAR"] = "wrong"

    with pytest.raises(ValueError):
        TestConfig()


def test_float_environment_variable():
    class TestConfig(OOConfig):
        VAR = FloatEnvironmentVariable()

    os.environ["VAR"] = "1.34"

    test_config = TestConfig()
    assert test_config.VAR == 1.34


def test_bad_float_environment_variable():
    class TestConfig(OOConfig):
        VAR = FloatEnvironmentVariable()

    os.environ["VAR"] = "wrong"

    with pytest.raises(ValueError):
        TestConfig()


def test_bool_environment_variable():
    class TestConfig(OOConfig):
        VAR_1 = BoolEnvironmentVariable()
        VAR_2 = BoolEnvironmentVariable()
        VAR_3 = BoolEnvironmentVariable()
        VAR_4 = BoolEnvironmentVariable()
        VAR_5 = BoolEnvironmentVariable()
        VAR_6 = BoolEnvironmentVariable()

    os.environ["VAR_1"] = "True"
    os.environ["VAR_2"] = "true"
    os.environ["VAR_3"] = "trUe"
    os.environ["VAR_4"] = "False"
    os.environ["VAR_5"] = "false"
    os.environ["VAR_6"] = "faLSe"

    test_config = TestConfig()
    assert test_config.VAR_1 and test_config.VAR_2 and test_config.VAR_3
    assert not(test_config.VAR_4 or test_config.VAR_5 or test_config.VAR_6)


def test_bad_bool_environment_variable():
    class TestConfig(OOConfig):
        VAR = BoolEnvironmentVariable()

    os.environ["VAR"] = "wrong"

    with pytest.raises(ValueError):
        TestConfig()

import os
from typing import Union, Callable


class EnvironmentVariable:
    def __init__(
            self,
            variable_name: str = None,
            *,
            prefix: str = "XX",
            default: Union[str, bool, int, float] = None,
            formatter: Callable = lambda x: x
    ):
        self.variable_name = variable_name
        self.default = default
        self.prefix = prefix
        self.formatter = formatter

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.attribute_name) or self.default

    def __set__(self, instance, value):
        instance.__dict__[self.attribute_name] = value

    def __set_name__(self, owner, name):
        self.attribute_name = "{}_{}".format(self.prefix, name)
        if self.variable_name is None:
            self.variable_name = name

    def load_from_env(self, instance):
        value_from_environment = os.getenv(self.variable_name)
        if value_from_environment is not None:
            try:
                instance.__dict__[self.attribute_name] = self.formatter(value_from_environment)
            except ValueError as e:
                raise ValueError(
                    "Error while loading {}('{}') : {}".format(
                        self.__class__.__name__, self.variable_name, " ".join(e.args))
                )
        elif self.default is not None:
            instance.__dict__[self.attribute_name] = self.default
        else:
            raise ValueError("No value nor default set for {}('{}')".format(
                self.__class__.__name__, self.variable_name)
            )


class IntEnvironmentVariable(EnvironmentVariable):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs, formatter=int)


class FloatEnvironmentVariable(EnvironmentVariable):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs, formatter=float)


class BoolEnvironmentVariable(EnvironmentVariable):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs, formatter=BoolEnvironmentVariable.cast_to_bool)

    @staticmethod
    def cast_to_bool(value: str) -> bool:
        if isinstance(value, str):
            if value.lower() == "true":
                return True
            elif value.lower() == "false":
                return False
        raise ValueError(
            "invalid value provided '{}'. Value should verify `value.lower() in ['true', 'false']`".format(value)
        )


class OOConfig:
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        for attribute in type(instance).__dict__.values():
            if isinstance(attribute, EnvironmentVariable):
                attribute.load_from_env(instance)
        return instance

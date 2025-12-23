import allure
import types


def allure_steps(cls):
    for attr in cls.__dict__:
        if isinstance(getattr(cls, attr), types.FunctionType) and not attr.startswith("_"):
            setattr(cls, attr, allure.step(getattr(cls, attr)))
    return cls
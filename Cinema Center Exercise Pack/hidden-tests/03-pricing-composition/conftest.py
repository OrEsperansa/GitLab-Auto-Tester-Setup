import importlib

import pytest


@pytest.fixture
def load_module():
    def _load_module(module_name):
        return importlib.import_module(module_name)

    return _load_module

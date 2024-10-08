from __future__ import annotations

import importlib.metadata

import pbpl_test as m


def test_version():
    assert importlib.metadata.version("pbpl_test") == m.__version__

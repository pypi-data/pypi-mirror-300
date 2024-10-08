from __future__ import annotations

import importlib.metadata

import pbpl_warpx as m


def test_version():
    assert importlib.metadata.version("pbpl_warpx") == m.__version__

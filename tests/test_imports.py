import importlib

from fastapi import FastAPI


def test_proxy_app_import_smoke() -> None:
    module = importlib.import_module("apps.proxy.main")

    assert isinstance(module.app, FastAPI)
    assert callable(module.create_app)

import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import importlib
import os

import pytest


def reload_config(monkeypatch, **env_vars):
    for key, value in env_vars.items():
        if value is None:
            monkeypatch.delenv(key, raising=False)
        else:
            monkeypatch.setenv(key, value)
    import config as cfg
    return importlib.reload(cfg)


def test_default_model(monkeypatch):
    cfg = reload_config(monkeypatch, DEFAULT_MODEL=None)
    assert cfg.Config.DEFAULT_MODEL == "nemo-llama3-8b"


def test_environment_override(monkeypatch):
    cfg = reload_config(monkeypatch, DEFAULT_MODEL="custom-model")
    assert cfg.Config.DEFAULT_MODEL == "custom-model"


def test_testing_config(monkeypatch):
    cfg = reload_config(monkeypatch)
    test_cfg = cfg.TestingConfig()
    assert test_cfg.TESTING is True
    assert test_cfg.CHROMA_PERSIST_DIRECTORY == "./test_chroma_db"

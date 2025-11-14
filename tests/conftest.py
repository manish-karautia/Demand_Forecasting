# tests/conftest.py
import os
import sys
import pytest

# Ensure repo root in PYTHONPATH
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import create_app

@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["LOGIN_DISABLED"] = True   # Makes login_required ignore authentication
    return app

@pytest.fixture
def client(app):
    return app.test_client()

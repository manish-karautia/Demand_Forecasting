import json
from run import app
from app.database import User


"""
def test_home():
    client = app.test_client()
    res = client.get("/")
    assert res.status_code == 200

def test_predict_monkeypatch(monkeypatch):
    class FakeModel:
        def predict(self, X):
            return [3.14]

    # patch get_models so real models are not loaded
    monkeypatch.setattr('run.get_models', lambda: {'clf': FakeModel()})

    client = app.test_client()
    payload = {"features": [1,2,3]}
    res = client.post("/predict", json=payload)
    assert res.status_code == 200
    assert res.get_json()["prediction"] == 3.14
"""

# tests/test_app.py

def test_home(client):
    res = client.get("/")
    assert res.status_code == 200


def test_predict_monkeypatch(monkeypatch, client):
    class FakeModel:
        def forecast(self, X):
            return [3.14]

    # Override your real models (so TensorFlow is not required in tests)
    monkeypatch.setattr("app.routes.regressor_model", FakeModel())
    monkeypatch.setattr("app.routes.classifier_model", FakeModel())

    res = client.post(
        "/predict",
        data={"country": "Ghana", "medicine": "Family Planning and Reproduction"},
        follow_redirects=True
    )

    assert res.status_code in (200, 302)


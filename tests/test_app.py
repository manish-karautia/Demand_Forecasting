import json
from run import app

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


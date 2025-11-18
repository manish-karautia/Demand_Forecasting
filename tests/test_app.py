import json
from run import app


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

"""
# tests/test_app.py
import pytest

def test_home(client):
    res = client.get("/")
    assert res.status_code == 200


def test_predict_monkeypatch(monkeypatch, client):
    class FakeModel:
        def forecast(self, X):
            return [3.14]

    # Inject fake models so TensorFlow is not loaded during tests
    monkeypatch.setattr("app.routes.regressor_model", FakeModel())
    monkeypatch.setattr("app.routes.classifier_model", FakeModel())

    res = client.post(
        "/predict",
        data={"country": "Ghana", "medicine": "Family Planning and Reproduction"},
        follow_redirects=True
    )

    assert res.status_code in (200, 302)
"""


# tests/test_app.py
import pytest
from flask_login import AnonymousUserMixin

def test_home(client):
    res = client.get("/")
    assert res.status_code == 200


def test_predict_monkeypatch(monkeypatch, client):

    class FakeUser:
        id = 1
        is_authenticated = True

    monkeypatch.setattr("app.routes.current_user", FakeUser())

    # -------------------------------
    # Fake models
    # -------------------------------
    class FakeModel:
        def forecast(self, X): return [3.14]
        def predict(self, X, verbose=0): return [[3.14]]

    monkeypatch.setattr("app.routes.regressor_model", FakeModel())
    monkeypatch.setattr("app.routes.classifier_model", FakeModel())

    # -------------------------------
    # Fake DB query and Prediction model
    # -------------------------------
    class FakeQuery:
        def filter(self, *args, **kwargs): return self
        def filter_by(self, *args, **kwargs): return self
        def order_by(self, *args, **kwargs): return self
        def limit(self, n): return self
        def all(self): return []
        def first(self): return None

    class FakePrediction:
        # Required attributes
        user_id = 1
        country = "Ghana"
        medicine = "Family Planning and Reproduction"
        timestamp = None  
        predicted_demand = "100 units"
        
    class FakeColumn:
        """A dummy column that supports .asc() and comparisons."""
        def asc(self):
            return self
        def __lt__(self, other):
            return True    # Always pass the filter condition
  

    class FakeQuery:
        def filter(self, *args, **kwargs): return self
        def filter_by(self, *args, **kwargs): return self
        def order_by(self, *args, **kwargs): return self
        def limit(self, n): return self
        def all(self): return []
        def first(self): return None


    class FakePrediction:
        # Fake SQLAlchemy columns
        timestamp = FakeColumn()
        user_id = FakeColumn()
        country = FakeColumn()
        medicine = FakeColumn()    
    
    

        # Attach fake query
        query = FakeQuery()

        def __init__(self, **kwargs):
            pass

    monkeypatch.setattr("app.routes.Prediction", FakePrediction)

    # -------------------------------
    # Perform request
    # -------------------------------
    res = client.post(
        "/predict",
        data={"country": "Ghana", "medicine": "Family Planning and Reproduction"},
        follow_redirects=True
    )

    assert res.status_code in (200, 302)




# -------------------------------------------------
# Fake Prediction model for the test environment
# -------------------------------------------------
class FakePrediction:
    """A minimal fake replacement for the SQLAlchemy Prediction model."""
    country = ""
    medicine = ""
    predicted_demand = "10 units"
    timestamp = None
    user_id = 1

    def __init__(self, country="", medicine="", predicted_demand="", user_id=1):
        self.country = country
        self.medicine = medicine
        self.predicted_demand = predicted_demand
        self.user_id = user_id

    @staticmethod
    def query():
        class FakeQuery:
            def filter_by(self, **kwargs):
                return self

            def order_by(self, *args, **kwargs):
                return self

            def all(self):
                return []
        return FakeQuery()

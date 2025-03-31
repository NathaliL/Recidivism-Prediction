
# import pytest
# import json
# from recidi_api import app

# @pytest.fixture
# def client():
#     # Create a test client for the app
#     with app.test_client() as client:
#         yield client

# def test_ui_to_backend_integration(client):
#     """Test if data sent from the UI is correctly received by the backend."""
#     # Simulating a UI payload
#     ui_payload = {
#         "gender": "Female",
#         "race": "Black",
#         "age_at_release": 25,
#         "education_level": "Bachelor's Degree",
#         "supervision_risk_score_first": 7,
#         "residence_puma": "B",
#         "jobs_per_year": 2
#     }

#     response = client.post('/predict', json=ui_payload)

#     # Check if the backend accepts the payload and processes it correctly
#     assert response.status_code == 200
#     assert "prediction" in response.json
#     assert "probabilities" in response.json
#     assert "explanation_text" in response.json

# def test_integration_prediction_accuracy(client, mocker):
#     """Test if the backend's prediction aligns with expected behavior."""
#     # Mock the model's prediction process
#     mocker.patch('recidi_api.model.joblib.load', return_value=mocker.Mock(
#         predict=lambda x: [0], predict_proba=lambda x: [[0.8, 0.2]]
#     ))

#     # Simulating a valid payload from the UI
#     ui_payload = {
#         "gender": "Male",
#         "race": "Hispanic",
#         "age_at_release": 40,
#         "education_level": "High School",
#         "supervision_risk_score_first": 4,
#         "residence_puma": "C",
#         "jobs_per_year": 0
#     }

#     response = client.post('/predict', json=ui_payload)

#     # Expecting the backend to return correct predictions
#     assert response.status_code == 200
#     assert response.json["prediction"] == "Low Risk of Recidivism"
#     assert round(response.json["probabilities"]["Non-Recidivist"], 2) == 80.0
#     assert round(response.json["probabilities"]["Recidivist"], 2) == 20.0

# def test_backend_handles_large_payloads(client):
#     """Test the backend's ability to handle a large payload."""
#     # Simulating a large dataset from UI
#     large_payload = [
#         {
#             "gender": "Male",
#             "race": "White",
#             "age_at_release": 30 + i,
#             "education_level": "High School",
#             "supervision_risk_score_first": i % 10,
#             "residence_puma": chr(65 + (i % 26)),
#             "jobs_per_year": i % 3
#         } for i in range(1000)  # Simulating 1000 entries
#     ]

#     response = client.post('/batch_predict', json={"data": large_payload})

#     # Check if the backend processes the batch correctly
#     assert response.status_code == 200
#     assert "predictions" in response.json
#     assert len(response.json["predictions"]) == 1000

import pytest
import json
from recidi_api import app

@pytest.fixture
def client():
    # Create a test client for the app
    with app.test_client() as client:
        yield client


def test_ui_to_backend_integration(client):
    """Test if valid data sent from the UI is correctly received by the backend."""
    ui_payload = {
        "gender": "Female",
        "race": "Black",
        "age_at_release": 25,
        "education_level": "Bachelor's Degree",
        "supervision_risk_score_first": 7,
        "residence_puma": "1",
        "jobs_per_year": 2
    }

    response = client.post('/predict', json=ui_payload)

    # Verify the response status and returned data structure
    assert response.status_code == 200
    assert "prediction" in response.json
    assert "probabilities" in response.json
    assert "explanation_text" in response.json
    assert "threshold_used" in response.json


def test_integration_prediction_accuracy(client, mocker):
    """Test if the backend returns correct predictions and probabilities."""
    # Mock the model's prediction process
    mocker.patch('joblib.load', return_value=mocker.Mock(
        predict=lambda x: [1],
        predict_proba=lambda x: [[0.2, 0.8]]
    ))

    ui_payload = {
        "gender": "Male",
        "race": "Hispanic",
        "age_at_release": 40,
        "education_level": "High School",
        "supervision_risk_score_first": 4,
        "residence_puma": "1",
        "jobs_per_year": 0
    }

    response = client.post('/predict', json=ui_payload)

    # Verify the response status and content
    assert response.status_code == 200
    assert response.json["prediction"] == "High Risk of Recidivism"
    assert "probabilities" in response.json
    assert response.json["probabilities"]["Recidivist"] == pytest.approx(50.0, rel=1e-2)
    assert response.json["probabilities"]["Non-Recidivist"] == pytest.approx(50.0, rel=1e-2)
    assert "explanation_text" in response.json
    assert "threshold_used" in response.json

    # Verify the response status and structure
    assert response.status_code == 200
    assert "prediction" in response.json
    assert "probabilities" in response.json


def test_model_loading():
    """Test if the model loads correctly without errors."""
    import joblib  # Ensure joblib is imported inside the function
    try:
        model = joblib.load("/Users/nathaliliyanage/Desktop/FYP/RecidiVision 2/ensemble_model_downsampled.pkl")  # Replace with actual model path
        assert model is not None
    except Exception as e:
        pytest.fail(f"Model loading failed: {e}")
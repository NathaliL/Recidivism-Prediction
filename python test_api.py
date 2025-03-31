import requests
import unittest

class TestUIBackendIntegration(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000/predict"  # Backend endpoint
    HEADERS = {
        "Content-Type": "application/json",
        "Origin": "http://localhost:3000",  # Frontend origin
        "Accept": "application/json"
    }

    def log_request_and_response(self, payload, response):
        """Helper to log request and response details for debugging."""
        print("===== Request =====")
        print(f"URL: {self.BASE_URL}")
        print(f"Payload: {payload}")
        print("===== Response =====")
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Response Body: {response.text}")
        print("=====================")

    def test_ui_to_backend_interaction(self):
        """Verify the interaction between the UI and backend by sending valid data."""
        # Payload based on the request received in logs
        payload = {
            "gender": "F",
            "race": "Hispanic",
            "age_at_release": 56,  # Convert age to an integer
            "education_level": "Associate Degree",
            "supervision_risk_score_first": 4,  # Convert score to an integer
            "residence_puma": "3",
            "jobs_per_year": 1.0  # Convert jobs_per_year to a float
        }

        # Send POST request
        response = requests.post(self.BASE_URL, json=payload, headers=self.HEADERS)

        # Log the request and response
        self.log_request_and_response(payload, response)

        # Check the response
        if response.status_code != 200:
            print("Error: Unexpected status code received.")
            self.fail(f"Expected status code 200 but got {response.status_code}. Check the logs for details.")

        # Parse the JSON response
        try:
            json_response = response.json()
        except ValueError:
            self.fail("Failed to parse JSON response. Response text: " + response.text)

        # Assertions for the expected keys in the response
        self.assertIn("prediction", json_response, "The backend response is missing the 'prediction' key.")
        self.assertIn("probabilities", json_response, "The backend response is missing the 'probabilities' key.")
        self.assertIn("explanation_text", json_response, "The backend response is missing the 'explanation_text' key.")

if __name__ == "__main__":
    unittest.main()

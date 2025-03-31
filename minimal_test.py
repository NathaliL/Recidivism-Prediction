import requests
import time
import json

TARGET_URL = "http://127.0.0.1:5000/predict"
SAMPLE_DATA = {
    "gender": "Male",
    "race": "White",
    "age_at_release": 30,
    "education_level": "High School",
    "supervision_risk_score_first": 5,
    "residence_puma": "12345",
    "jobs_per_year": 2
}

# Minimal headers matching the successful curl command
HEADERS = {
    "Content-Type": "application/json",
    "Origin": "http://localhost:3000",
    "Referer": "http://localhost:3000/",
    "User-Agent": "Mozilla/5.0"
}

def send_request():
    try:
        # Force compact JSON formatting to mimic curl
        data_str = json.dumps(SAMPLE_DATA, separators=(',', ':'))
        start_time = time.time()
        response = requests.post(TARGET_URL, data=data_str, headers=HEADERS)
        duration = time.time() - start_time
        return duration, response.status_code, response.text
    except Exception as e:
        return -1, f"Error: {e}", ""

if __name__ == "__main__":
    duration, status, text = send_request()
    print(f"Response Time: {duration:.2f}s, Status Code: {status}")
    print("Response Text:", text)

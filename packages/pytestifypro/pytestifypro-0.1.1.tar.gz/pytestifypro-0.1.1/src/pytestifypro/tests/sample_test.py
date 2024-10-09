# src/pytestifypro/tests/test_sample.py
import pytest
import requests
import logging

@pytest.mark.test
def test_sample_response():
    url = "http://localhost:8081/api/test"
    response = requests.get(url)
    logging.info(f"Response Status Code: {response.status_code}")
    logging.info(f"Response Body: {response.text}")
    assert response.status_code == 200
    assert response.json() == {"message": "This is a sample response from wiremock"}

@pytest.mark.xfail
def test_not_found_response():
    response = requests.get("http://localhost:8081/api/unknown")
    assert response.status_code == 200 #404
import pytest

from pytestifypro.data.data_loader import load_schema
from pytestifypro.utils.utils import (
    format_url, validate_json_schema, log_response_time, retry_request
)
import requests
from requests.exceptions import RequestException


def format_url_with_params(base_url, endpoint, **params):
    """
    Format a URL with parameters.
    """
    return base_url.rstrip('/') + endpoint.format(**params)

# Example usage
url = format_url_with_params("https://api.example.com", "/users/{user_id}", user_id=123)


def test_format_url():
    assert format_url("http://example.com", "/test") == "http://example.com/test"
    assert format_url("http://example.com/", "test") == "http://example.com/test"
    assert format_url(None, "test") is None

@pytest.mark.xfail
def test_validate_json_schema():
    # Load schema from config
    schema_config = load_schema()
    schema = schema_config.get('user_schema')

    # Valid case
    assert validate_json_schema({"name": "John"}, schema) is True

    # Valid case (contains both required and optional fields)
    assert validate_json_schema({"name": "John", "age": 30}, schema) is True

    # Invalid case (missing required 'name' property)
    assert validate_json_schema({"age": 30}, schema) is True

def test_log_response_time(mocker):
    mocker.patch('requests.get', return_value=requests.Response())
    mock_request_func = mocker.MagicMock(return_value=requests.get("http://example.com"))
    response = log_response_time(mock_request_func, "http://example.com")
    assert response is not None

def test_retry_request(mocker):
    # Mock the request_func to always raise a RequestException
    mock_request_func = mocker.MagicMock(side_effect=RequestException("Connection error"))

    # Call retry_request with the mock_request_func
    response = retry_request(mock_request_func, retries=3, url="http://example.com")

    # Assert that the response is None after retries
    assert response is None
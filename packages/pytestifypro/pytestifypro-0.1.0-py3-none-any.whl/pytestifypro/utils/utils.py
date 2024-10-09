import logging
import time
from urllib.parse import urlencode

import requests
import yaml
from jsonschema import validate, ValidationError

def log_info(message):
    """Log an informational message."""
    logging.info(message)

def log_warning(message):
    """Log a warning message."""
    logging.warning(message)

def log_error(message):
    """Log an error message."""
    logging.error(message)

def log_critical(message):
    """Log a critical error message."""
    logging.critical(message)


def format_url(base_url, endpoint, params=None):
    """
    Format URL by combining base URL and endpoint, and optionally appending query parameters.

    Parameters:
    - base_url (str): The base URL.
    - endpoint (str): The API endpoint.
    - params (dict): Query parameters to append to the URL.

    Returns:
    - str: The formatted URL.
    """
    if base_url is None or endpoint is None:
        log_error("Base URL or endpoint is None")
        return None

    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    if params:
        query_string = urlencode(params)
        url = f"{url}?{query_string}"

    return url

def validate_json_schema(response_json, schema):
    """Validate a JSON response against a schema."""
    try:
        validate(instance=response_json, schema=schema)
        log_info("JSON schema validation passed.")
        return True, None
    except ValidationError as e:
        log_error(f"JSON schema validation failed: {e.message}")
        return False, e.message

def send_get_request(session, url, headers=None, params=None, timeout=None):
    response = session.get(url, headers=headers, params=params, timeout=timeout)
    response.raise_for_status()
    return response

def send_post_request(session, url, headers=None, data=None, json=None, timeout=None):
    response = session.post(url, headers=headers, data=data, json=json, timeout=timeout)
    response.raise_for_status()
    return response

def send_put_request(session, url, headers=None, data=None, json=None, timeout=None):
    response = session.put(url, headers=headers, data=data, json=json, timeout=timeout)
    response.raise_for_status()
    return response

def send_delete_request(session, url, headers=None, timeout=None):
    response = session.delete(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response

def log_response_time(request_func, *args, **kwargs):
    """Logs the response time of an API request."""
    start_time = time.time()
    response = request_func(*args, **kwargs)
    end_time = time.time()
    log_info(f"Response time: {end_time - start_time:.2f} seconds")
    return response

def retry_request(request_func, retries=3, backoff_factor=0.3, *args, **kwargs):
    """Retries an API request in case of failure."""
    for attempt in range(retries):
        try:
            response = request_func(*args, **kwargs)
            if response and response.ok:  # Ensure response is not None and is successful
                return response
        except requests.RequestException as e:
            sleep_time = backoff_factor * (2 ** attempt)
            log_warning(f"Request failed: {e}. Retrying... ({attempt+1}/{retries})")
    log_critical(f"Request failed after {retries} attempts.")
    return None

def get_json_attribute(data, path, default=None):
    """
    Fetch a specific attribute from a JSON object using a path.

    Parameters:
    - data (dict): The JSON object.
    - path (str): The dot-separated path to the attribute.
    - default: The default value to return if the path is not found.

    Returns:
    - The value found at the specified path, or the default value.
    """
    keys = path.split('.')
    for key in keys:
        if not isinstance(data, dict) or key not in data:
            log_warning(f"Key '{key}' not found in path '{path}'. Returning default value.")
            return default
        data = data[key]
    return data


def extract_values_from_json_array(data, key):
    """
    Extracts a list of values from an array of JSON objects.
    Example: [{"name": "John"}, {"name": "Doe"}], key="name" returns ["John", "Doe"]
    """
    return [item.get(key) for item in data if key in item]

def load_schema(file_path='src/pytestifypro/config/schema_config.yaml'):
    """
    Load the JSON schema from the YAML configuration file and validate it.

    Parameters:
    - file_path (str): Path to the YAML file containing the schema.

    Returns:
    - dict: The loaded schema if successful.
    """
    try:
        with open(file_path, 'r') as file:
            schema = yaml.safe_load(file)
            if not isinstance(schema, dict):
                log_error(f"Invalid schema format in file: {file_path}")
                return None
            return schema
    except FileNotFoundError:
        log_error(f"Schema file not found at: {file_path}")
        return None
    except yaml.YAMLError as e:
        log_error(f"Error parsing YAML file at {file_path}: {e}")
        return None
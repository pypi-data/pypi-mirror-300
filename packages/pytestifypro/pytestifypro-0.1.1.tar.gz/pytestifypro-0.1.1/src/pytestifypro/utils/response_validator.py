# src/pytestifypro/utils/response_validator.py

from pytestifypro.utils.utils import log_info

class ResponseValidator:
    def __init__(self, response):
        self.response = response

    def validate_status_code(self, expected_status_code: int):
        actual_status_code = self.response.status_code
        log_info(f"Validating status code: expected {expected_status_code}, got {actual_status_code}")
        assert actual_status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {actual_status_code}"

    def validate_field(self, expected_value, actual_value, field_name: str):
        log_info(f"Validating field '{field_name}': expected {expected_value}, got {actual_value}")
        assert expected_value == actual_value, f"Expected {field_name} '{expected_value}', but got '{actual_value}'"

    def validate_response_message(self, expected_message: str):
        actual_message = self.response.json().get("message", "")
        log_info(f"Validating response message: expected '{expected_message}', got '{actual_message}'")
        assert actual_message == expected_message, f"Expected message '{expected_message}', but got '{actual_message}'"

    # Add more validation methods as needed...

# src/pytestifypro/client/api_client.py

import logging
import requests
from requests.exceptions import HTTPError, Timeout
from pytestifypro.utils.utils import (
    send_get_request, send_post_request, send_put_request, send_delete_request, retry_request
)
from pytestifypro.data.data_loader import load_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url=None, config_file='src/pytestifypro/config/config.yaml'):
        """
        Initialize the APIClient with a base URL and optional headers.
        :param base_url: Base URL for the API client. If None, uses the config file.
        :param config_file: Path to the configuration YAML file.
        """
        self.session = requests.Session()
        self.timeout = 10  # Default timeout of 10 seconds
        self.headers = {}  # Initialize headers to an empty dictionary

        # Load configuration
        if base_url:
            self.base_url = base_url.rstrip('/')
        else:
            config = load_config(config_file)
            self.base_url = config.get('base_url', '').rstrip('/')
            self.headers = config.get('headers', {})
            self.timeout = config.get('timeout', self.timeout)  # Optional timeout from config

        logger.info(f"Initialized APIClient with base URL: {self.base_url}")

    def _create_url(self, endpoint: str) -> str:
        """
        Create the full URL by combining the base URL and the endpoint.
        :param endpoint: The API endpoint.
        :return: The full URL.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug(f"Created URL: {url}")
        return url

    def _handle_response(self, response: requests.Response):
        """
        Handle HTTP response, raising exceptions for error status codes.
        :param response: Response object.
        """
        try:
            response.raise_for_status()  # Will raise HTTPError for 4xx/5xx responses
        except HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
            raise
        except Exception as err:
            logger.error(f"Unexpected error occurred: {err}")
            raise
        return response

    def get(self, endpoint: str, params: dict = None):
        """
        Perform a GET request.
        :param endpoint: The API endpoint.
        :param params: Optional query parameters.
        :return: Response object.
        """
        url = self._create_url(endpoint)
        logger.info(f"Performing GET request to {url} with params: {params}")
        try:
            response = retry_request(lambda: send_get_request(self.session, url, headers=self.headers, params=params,
                                     timeout=self.timeout))
            return self._handle_response(response)
        except Timeout:
            logger.error(f"GET request to {url} timed out after {self.timeout} seconds.")
            return None

    def post(self, endpoint: str, data: dict = None, json: dict = None):
        """
        Perform a POST request.
        :param endpoint: The API endpoint.
        :param data: Data to send in the body of the request.
        :param json: JSON data to send in the body of the request.
        :return: Response object.
        """
        url = self._create_url(endpoint)
        logger.info(f"Performing POST request to {url} with data: {data} and json: {json}")
        try:
            response = retry_request(
                lambda: send_post_request(self.session, url, headers=self.headers, data=data, json=json, timeout=self.timeout)
            )
            return self._handle_response(response)
        except Timeout:
            logger.error(f"POST request to {url} timed out after {self.timeout} seconds.")
            return None

    def put(self, endpoint: str, data: dict = None, json: dict = None):
        """
        Perform a PUT request.
        :param endpoint: The API endpoint.
        :param data: Data to send in the body of the request.
        :param json: JSON data to send in the body of the request.
        :return: Response object.
        """
        url = self._create_url(endpoint)
        logger.info(f"Performing PUT request to {url} with data: {data} and json: {json}")
        try:
            response = retry_request(
                lambda: send_put_request(self.session, url, headers=self.headers, data=data, json=json, timeout=self.timeout)
            )
            return self._handle_response(response)
        except Timeout:
            logger.error(f"PUT request to {url} timed out after {self.timeout} seconds.")
            return None

    def delete(self, endpoint: str):
        """
        Perform a DELETE request.
        :param endpoint: The API endpoint.
        :return: Response object.
        """
        url = self._create_url(endpoint)
        logger.info(f"Performing DELETE request to {url}")
        try:
            response = retry_request(
                lambda: send_delete_request(self.session, url, headers=self.headers, timeout=self.timeout)
                )
            return self._handle_response(response)
        except Timeout:
            logger.error(f"DELETE request to {url} timed out after {self.timeout} seconds.")
            return None

    def close(self):
        """
        Close the session to free up resources.
        """
        self.session.close()
        logger.info("Closed APIClient session")

import pytest
from pytestifypro.comparer.json_comparer import JSONComparer
from pytestifypro.utils.assertions import assert_no_differences
from pytestifypro.utils.response_validator import ResponseValidator

@pytest.mark.fintests
@pytest.mark.mock
def test_upi_payment_success(api_client, config, priority_manager, reporter, test_setup):
    test_setup("UPI Payment", "UPI Payment Success Scenario", "Verifies successful UPI payment", "critical")

    endpoint = config['endpoints']['upi_payment_status']
    payload = config['upi_payment']['success']['payload']
    expected_response = config['upi_payment']['success']['response']

    # API call
    response = api_client.post(endpoint, json=payload)

    # Validate the status code
    validator = ResponseValidator(response)
    validator.validate_status_code(200)

    # Compare the full JSON response
    comparer = JSONComparer(priority_manager, reporter)
    differences = comparer.compare(expected_response, response.json())

    # Assert that no differences exist
    assert_no_differences(differences)


@pytest.mark.fintests
@pytest.mark.mock
def test_upi_payment_failure(api_client, config, priority_manager, reporter, test_setup):
    test_setup("UPI Payment", "UPI Payment Failure Scenario", "Verifies failed UPI payment", "critical")
    endpoint = config['endpoints']['upi_payment_status']
    payload = config['upi_payment']['failure']['payload']
    expected_response = config['upi_payment']['failure']['response']

    # API call
    response = api_client.post(endpoint, json=payload)

    # Validate the status code
    validator = ResponseValidator(response)
    validator.validate_status_code(200)

    # Compare the full JSON response
    comparer = JSONComparer(priority_manager, reporter)
    differences = comparer.compare(expected_response, response.json())

    # Assert that no differences exist
    assert_no_differences(differences)


@pytest.mark.fintests
@pytest.mark.mock
def test_upi_payment_pending(api_client, config, priority_manager, reporter, test_setup):
    test_setup("UPI Payment", "UPI Payment Pending Scenario", "Verifies Pending UPI payment", "critical")
    endpoint = config['endpoints']['upi_payment_status']
    payload = config['upi_payment']['pending']['payload']
    expected_response = config['upi_payment']['pending']['response']

    # API call
    response = api_client.post(endpoint, json=payload)

    # Validate the status code
    validator = ResponseValidator(response)
    validator.validate_status_code(200)

    # Compare the full JSON response
    comparer = JSONComparer(priority_manager, reporter)
    differences = comparer.compare(expected_response, response.json())

    # Assert that no differences exist
    assert_no_differences(differences)

# src/pytestifypro/utils/assertions.py

from pytestifypro.utils.utils import log_info

def assert_no_differences(differences: list[str]):
    """
    Assert that there are no differences in the JSON comparison.
    Logs differences if found.
    """
    if differences:
        for diff in differences:
            log_info(f"Difference found: {diff}")

        assert not differences, "Unexpected differences found in the JSON response."

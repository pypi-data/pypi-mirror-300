from typing import Any, List
from ..managers.priority_manager import PriorityManager
from ..reporters.difference_reporter import DifferenceReporter


class JSONComparer:
    def __init__(self, priority_manager: PriorityManager, reporter: DifferenceReporter):
        self.priority_manager = priority_manager
        self.reporter = reporter

    def compare(self, expected: Any, actual: Any, path: str = "") -> List[str]:
        differences = []

        if isinstance(expected, dict) and isinstance(actual, dict):
            for key in expected:
                current_path = f"{path}.{key}" if path else key
                if key not in actual:
                    priority = self.priority_manager.get_priority(current_path)
                    differences.append(self.reporter.report_difference(current_path, f"Key '{key}' is missing in actual data", priority))
                else:
                    differences.extend(self.compare(expected[key], actual[key], current_path))
        elif isinstance(expected, list) and isinstance(actual, list):
            for index, item in enumerate(expected):
                current_path = f"{path}[{index}]"
                if index < len(actual):
                    differences.extend(self.compare(item, actual[index], current_path))
                else:
                    priority = self.priority_manager.get_priority(current_path)
                    differences.append(self.reporter.report_difference(current_path, f"Index {index} is missing in actual data", priority))
        else:
            if expected != actual:
                priority = self.priority_manager.get_priority(path)
                differences.append(self.reporter.report_difference(path, f"expected {expected}, got {actual}", priority))

        return differences

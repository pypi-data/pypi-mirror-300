# src/pytestifypro/difference_reporter.py

from abc import ABC, abstractmethod


class DifferenceReporter(ABC):
    @abstractmethod
    def report_difference(self, path: str, message: str, priority: str) -> str:
        pass


class SimpleDifferenceReporter(DifferenceReporter):
    def report_difference(self, path: str, message: str, priority: str) -> str:
        return f"{priority}: {message} at '{path}'"

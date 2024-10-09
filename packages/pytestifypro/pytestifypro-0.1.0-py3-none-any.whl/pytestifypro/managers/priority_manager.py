# src/pytestifypro/priority_manager.py

from abc import ABC, abstractmethod
from typing import Dict

import yaml


class PriorityManager(ABC):
    @abstractmethod
    def get_priority(self, path: str) -> str:
        pass


class SimplePriorityManager(PriorityManager):
    def __init__(self, priority_map_file: str, default_priority: str = "P3"):
        self.priority_map = self._load_priority_map(priority_map_file)
        self.default_priority = default_priority

    def _load_priority_map(self, file_path: str) -> Dict[str, str]:
        """Load priority map from a YAML file."""
        with open(file_path, 'r') as file:
            return yaml.safe_load(file) or {}

    def get_priority(self, path: str) -> str:
        return self.priority_map.get(path, self.default_priority)

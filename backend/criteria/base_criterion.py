from abc import ABC, abstractmethod

class BaseCriterion(ABC):
    @abstractmethod
    def analyze(self, file_path):
        """Analyze a single file and return results."""
        pass

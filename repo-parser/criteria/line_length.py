from criteria.base_criterion import BaseCriterion

class LineLengthCriterion(BaseCriterion):
    def __init__(self, max_length=80):
        self.max_length = max_length

    def analyze(self, file_path):
        issues = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file, start=1):
                if len(line.rstrip()) > self.max_length:
                    issues.append(f"Line {i}: Exceeds {self.max_length} characters")
        return issues

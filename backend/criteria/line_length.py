from criteria.base_criterion import BaseCriterion

class LineLengthCriterion(BaseCriterion):
    def __init__(self, max_length=80):
        self.max_length = max_length

    def analyze(self, file_path):
        issues = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for i, line in enumerate(file, start=1):
                    if len(line.rstrip()) > self.max_length:
                        issues.append(f"Line {i}: Exceeds {self.max_length} characters")
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin1') as file:
                    for i, line in enumerate(file, start=1):
                        if len(line.rstrip()) > self.max_length:
                           issues.append(f"Line {i}: Exceeds {self.max_length} characters")
            except Exception as e: # Catch other potential errors
                issues.append(f"Error processing {file_path}: {e}")
        except FileNotFoundError: # Catch the case where the file isn't found.
            issues.append(f"File not found: {file_path}")
        return issues

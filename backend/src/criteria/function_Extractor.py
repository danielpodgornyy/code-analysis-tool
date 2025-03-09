import re

class FunctionExtractor:
    def __init__(self):
        """Initialize FunctionExtractor."""
        self.functions = []

    def analyze(self, file_path):
        """Extracts and returns only the function names from a Python file."""
        self.functions = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            for line in lines:
                stripped_line = line.strip()

                # Extract function name using regex
                function_match = re.match(r'def\s+(\w+)', stripped_line)
                if function_match:
                    self.functions.append(function_match.group(1))  # Only store the function name

        except (UnicodeDecodeError, FileNotFoundError) as e:
            return [f"Error reading file {file_path}: {e}"]

        return self.functions

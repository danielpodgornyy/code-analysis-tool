import re

class ImportExtractor:
    def __init__(self):
        """Initialize ImportExtractor."""
        self.imports = []

    def analyze(self, file_path):
        """Extracts and returns only the import statements from a Python file."""
        self.imports = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            for line in lines:
                stripped_line = line.strip()

                # Correct regex to match full import statements
                if re.match(r'^\s*(import\s+\w+|from\s+\w+\s+import\s+[\w,*]+)', stripped_line):
                    self.imports.append(stripped_line)  # Store the full import line

        except (UnicodeDecodeError, FileNotFoundError) as e:
            return [f"Error reading file {file_path}: {e}"]

        return self.imports

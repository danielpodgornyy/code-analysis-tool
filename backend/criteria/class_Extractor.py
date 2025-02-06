import re

class ClassExtractor:
    def __init__(self):
        """Initialize ClassExtractor."""
        self.classes = []
    
    def analyze(self, file_path):
        """Extracts and returns only the class names from a Python file."""
        self.classes = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            for line in lines:
                stripped_line = line.strip()
                
                # Extract class name using regex
                class_match = re.match(r'class\s+(\w+)', stripped_line)
                if class_match:
                    self.classes.append(class_match.group(1))  # Only store the class name
            
        except (UnicodeDecodeError, FileNotFoundError) as e:
            return [f"Error reading file {file_path}: {e}"]

        return self.classes
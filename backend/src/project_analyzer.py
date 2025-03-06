import os
from flask import jsonify

from criteria.line_length import LineLengthCriterion
from config import CRITERIA

from criteria.class_Extractor import ClassExtractor
from criteria.function_Extractor import FunctionExtractor
from criteria.import_Extractor import ImportExtractor

class ProjectAnalyzer():
    def __init__(self, directory):
        self.directory = directory
        self.files = None
        self.analysis= None

        self.list_files_from_directory()
        self.analyze_files()

    def list_files_from_directory(self):
        """List all files in a directory, excluding hidden ones."""
        file_list = []
        for root, dirs, files in os.walk(self.directory):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if not file.startswith('.'):
                    relative_path = os.path.relpath(os.path.join(root, file), self.directory)
                    file_list.append(relative_path)

        self.files = file_list

    def analyze_files(self):
        """Analyze each file against enabled criteria."""
        results = {}
        for file_path in self.files:
            absolute_path = os.path.join(self.directory, file_path)
            results[file_path] = {}

            for criterion_name, criterion_config in CRITERIA.items():
                if criterion_config["enabled"]:
                    if criterion_name == "line_length":
                        checker = LineLengthCriterion(criterion_config["max_length"])
                        results[file_path][criterion_name] = checker.analyze(absolute_path)  # Pass the path

                    elif criterion_name == "class_extraction":
                        extractor = ClassExtractor()
                        results[file_path][criterion_name] = extractor.analyze(absolute_path)  # Pass the path

                    elif criterion_name == "function_extraction":
                        extractor = FunctionExtractor()
                        results[file_path][criterion_name] = extractor.analyze(absolute_path)  # Pass the path

                    elif criterion_name == "import_extraction":
                        extractor = ImportExtractor()
                        results[file_path][criterion_name] = extractor.analyze(absolute_path)  # Pass the path


            results[file_path]["summary"] = {key: val for key, val in results[file_path].items()}

        self.analysis = results

    def results(self):
        if not self.files:
            return jsonify({"error": "No files found in repository"}), 400
        elif not self.analysis:
            return jsonify({"error": "Could not analyze repository"}), 400

        return jsonify({"files": self.files, "analysis": self.analysis}), 200

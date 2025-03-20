import os
import re
from flask import jsonify

from criteria.line_length import LineLengthCriterion
from config import CRITERIA

from criteria.class_Extractor import ClassExtractor
from criteria.function_Extractor import FunctionExtractor
from criteria.import_Extractor import ImportExtractor
from function_parser import FunctionParser
from function_grader import FunctionGrader

class ProjectAnalyzer():
    def __init__(self, directory):
        if not isinstance(directory, str):
            raise TypeError(f"Expected string for temp_dir path")

        self.directory = directory
        self.files = None
        self.file_analysis = {}
        self.project_grades = []

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
        for file_path in self.files:
            # If its not a C file, continue
            if not re.match("^[\w,\s-]+\.[cC]$", file_path):
                continue

            # Create the absolute path from the filename and position
            absolute_path = os.path.join(self.directory, file_path)

            # The parser takes in the file path and outputs a list of objects containing the function name and body
            parser = FunctionParser(absolute_path)
            functions = parser.get_functions()

            # Using the result from the parser, we check the function criteria
            function_grader = FunctionGrader(functions)
            failed_criteria = function_grader.get_failed_criteria()
            file_grade = function_grader.calculate_file_grade(parser.get_file_length())

            # Object to send to overall view of project
            self.project_grades.append({
                'filename': file_path,
                'grade': file_grade
                })

            # Object to send to individual project analysis
            self.file_analysis[file_path] = {
                    'grade': file_grade,
                    'failed_criteria': failed_criteria
                    }


    def get_file_results(self, filename):
        return self.file_analysis[filename] if self.file_analysis else None

    def get_project_grades(self):
        return {'project_grades': self.project_grades} if self.project_grades else None

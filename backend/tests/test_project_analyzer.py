import pytest
import tempfile

from src.project_analyzer import ProjectAnalyzer

class TestProjectAnalyzer():
    def test_insert_number_returns_error(self, flask_app):
        with pytest.raises(TypeError):
            analyzer = ProjectAnalyzer(3)

    def test_insert_empty_directory_returns_None(self, flask_app):
        with tempfile.TemporaryDirectory() as temp_dir:
            analyzer = ProjectAnalyzer(temp_dir)
            assert analyzer.get_project_grades() == None


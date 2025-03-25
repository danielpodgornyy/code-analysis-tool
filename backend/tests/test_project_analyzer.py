import pytest
import tempfile

from src.project_analyzer import ProjectAnalyzer

class TestProjectAnalyzer():
    def test_insert_number_returns_error(self):
        with pytest.raises(TypeError):
            analyzer = ProjectAnalyzer(3)

    def test_insert_empty_directory_returns_None(self, tmp_path):
        analyzer = ProjectAnalyzer(str(tmp_path))
        assert analyzer.get_project_grades() == None


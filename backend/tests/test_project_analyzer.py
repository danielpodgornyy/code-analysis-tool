import pytest
import tempfile
import os
from src.project_analyzer import ProjectAnalyzer

def test_analyzer_rejects_non_string():
    analyzer = ProjectAnalyzer()
    with pytest.raises(TypeError):
        analyzer.analyze_directory(123)

def test_analyzer_handles_empty_folder(tmp_path):
    analyzer = ProjectAnalyzer()
    analyzer.analyze_directory(str(tmp_path))
    assert analyzer.get_project_grades() is None

def test_analyzer_processes_valid_c_file(tmp_path):
    c_code = """
    int main() {
        return 0;
    }
    """
    test_file = tmp_path / "test.c"
    test_file.write_text(c_code)

    analyzer = ProjectAnalyzer()
    analyzer.analyze_directory(str(tmp_path))

    grades = analyzer.get_project_grades()
    assert isinstance(grades, dict)
    assert 'project_grades' in grades
    assert len(grades['project_grades']) == 1

    filename = analyzer.files[0]
    file_result = analyzer.get_file_results(filename)
    assert file_result is not None
    assert 'grade' in file_result

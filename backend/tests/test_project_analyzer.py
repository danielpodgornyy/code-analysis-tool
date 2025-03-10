import pytest
import tempfile

from src.project_analyzer import ProjectAnalyzer

class TestProjectAnalyzer():
    def test_insert_number_returns_error(self, flask_app):
        with pytest.raises(TypeError):
            with flask_app.app_context():
                analyzer = ProjectAnalyzer(3)

    # REFRAIN FROM ADDING MORE TESTS UNTIL THE JSON IS MOVED TO THE APP PORTION, WE WANT THE PROJECT_ANALYZER TO ONLY RETURN THE OBJECTS, NOT THE JSONIFY DATA
    def test_insert_empty_directory_returns_error(self, flask_app):
        with tempfile.TemporaryDirectory() as temp_dir:

            with flask_app.app_context():
                analyzer = ProjectAnalyzer(temp_dir)

                print(analyzer.get_project_grades()[0].get_json())
                assert analyzer.get_project_grades()



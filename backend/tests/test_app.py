import pytest
import tempfile
import os
import shutil

class TestApp():
    def test_get_root_returns_404(self, client):
        response = client.get("/")
        assert b"404 Not Found" in response.data

    def test_get_random_url_returns_404(self, client):
        response = client.get("/fasfa")
        assert b"404 Not Found" in response.data

    def test_post_run_analyzer_with_empty_body_returns_error(self, client):
        response = client.post("/run-analyzer", json={})
        print(response)

        assert response.status_code == 400
        assert response.get_json().get("error") == "No repository URL provided"

    def test_post_run_analyzer_with_only_url_returns_project_grades(self, client):
        response = client.post("/run-analyzer", json={
            "repo_url": "https://github.com/danielpodgornyy/test"
            })

        assert response.status_code == 200

        json_data = response.get_json()
        assert json_data
        assert "project_grades" in json_data

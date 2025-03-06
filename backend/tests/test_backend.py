import pytest

class TestBackend():

    def test_get_root_returns_404(self, client):
        response = client.get("/")
        assert b"404 Not Found" in response.data

    def test_get_random_url_returns_404(self, client):
        response = client.get("/fasfa")
        assert b"404 Not Found" in response.data

    def test_post_run_analyzer_with_empty_body_returns_error(self, client):
        response = client.post("/run-analyzer", data={})
        print(response)

        assert response.status_code == 400
        assert response.get_json().get("error") == "Invalid request format"

    def test_post_run_analyzer_with_only_url_returns_analysis(self, client):
        response = client.post("/run-analyzer", data={
            "repo_url": "https://github.com/danielpodgornyy/netman"
            })

        print(response)

        #assert response.status_code == 200

# The main backend file

import os
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from git import Repo, exc
from criteria.line_length import LineLengthCriterion
from config import CRITERIA

app = Flask(__name__)
CORS(app, origins=["http://localhost:4200"])  # Allow requests from Angular app

def list_files_from_directory(directory):
    """List all files in a directory, excluding hidden ones."""
    file_list = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if not file.startswith('.'):
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                file_list.append(relative_path)
    return file_list

def analyze_files(directory, file_list):
    """Analyze each file against enabled criteria."""
    results = {}
    for file_path in file_list:
        absolute_path = os.path.join(directory, file_path)
        results[file_path] = {}
        for criterion_name, criterion_config in CRITERIA.items():
            if criterion_config["enabled"]:
                if criterion_name == "line_length":
                    checker = LineLengthCriterion(criterion_config["max_length"])
                    results[file_path][criterion_name] = checker.analyze(absolute_path)
    return results

@app.route("/run-analyzer", methods=["POST"])
def run_analyzer():
    try:
        # Check if the body is JSON
        if request.is_json:
            data = request.get_json()  # Parse the incoming JSON
            repo_url_or_path = data.get("repo_url")  # Extract the repo_url field

            if not repo_url_or_path:
                return jsonify({"error": "No repository URL or local path provided"}), 400

            # If it's a local path, process directly
            if os.path.isdir(repo_url_or_path):  # It's a local directory
                directory = repo_url_or_path
                file_list = list_files_from_directory(directory)
                if not file_list:
                    return jsonify({"error": "No files found in the directory."}), 400

                analysis_results = analyze_files(directory, file_list)

                return jsonify({"files": file_list, "analysis": analysis_results}), 200

            # Otherwise, assume it's a URL and clone the repository
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"Cloning repository from {repo_url_or_path} into {temp_dir}...")

                try:
                    repo = Repo.clone_from(repo_url_or_path, temp_dir)

                    if repo.bare:
                        return jsonify({"error": "The repository is bare or invalid."}), 400

                    repo.git.checkout()
                    directory = temp_dir

                    # List files and analyze them inside the temporary directory scope
                    file_list = list_files_from_directory(directory)
                    if not file_list:
                        return jsonify({"error": "No files found in the repository."}), 400

                    analysis_results = analyze_files(directory, file_list)

                    return jsonify({"files": file_list, "analysis": analysis_results}), 200

                except exc.GitCommandError as e:
                    return jsonify({"error": f"Failed to clone repository: {e.stderr.strip()}"}), 500

        else:
            return jsonify({"error": "Request is not JSON"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

import os
import tempfile
import zipfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from git import Repo, exc

from src.project_analyzer import ProjectAnalyzer

app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:4200",
    "https://codeanalysis-42512.web.app",
    "https://codeanalysis-42512.firebaseapp.com",
    "https://code-analysis-a27ff.web.app",
    "https://code-analysis-a27ff.firebaseapp.com"
])

# Analyzer which saves information between calls
analyzer = ProjectAnalyzer()

@app.route("/run-analyzer", methods=["POST"])
def run_analyzer():
    """Handles the preliminary checks on the input data, creates a temporary directory, clones the data from the repo or zip and passes off the directory to the project analyzer, then it takes the result and gives it to the client"""

    try:
        # Handles a url
        if request.is_json:
            repo_url = request.get_json().get('repo_url')

            # Check if a url has been provided
            if not repo_url:
                return jsonify({"error": "No repository URL provided"}), 400

            # Copy the github repo into a temporary directory and perform analysis operations
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"Cloning repository from {repo_url} into {temp_dir}...")

                try:
                    repo = Repo.clone_from(repo_url, temp_dir)

                    if repo.bare:
                        return jsonify({"error": "The repository is bare or invalid."}), 400

                    # ProjectAnalyzer handles all intermediate analysis steps
                    analyzer.analyze_directory(temp_dir)

                    # Pull the grade list from the project and return it
                    grades = analyzer.get_project_grades()

                    if grades:
                        return jsonify(grades), 200
                    return jsonify({'error': 'There are no files to grade'}), 500
                except exc.GitCommandError as e:
                    return jsonify({"error": f"Failed to clone repository: {e.stderr.strip()}"}), 500

        # Handles a zip file
        elif 'file' in request.files:
            uploaded_file = request.files['file']

            # Only accepts zip files
            if not uploaded_file.filename.endswith('.zip'):
                return jsonify({"error": "Only .zip files are allowed"}), 400

            # Copy the zip file contents
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = os.path.join(temp_dir, uploaded_file.filename)
                uploaded_file.save(zip_path)

                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)

                    # ProjectAnalyzer handles all intermediate analysis steps
                    analyzer.analyze_directory(temp_dir)

                    # Pull the grade list from the project and return it
                    grades = analyzer.get_project_grades()

                    if grades:
                        return jsonify(grades), 200
                    return jsonify({'error': 'There are no files to grade'}), 500
                except zipfile.BadZipFile:
                    return jsonify({"error": "The uploaded file is not a valid ZIP file."}), 400
                except Exception as e:
                    return jsonify({"error": f"An error occurred while extracting the ZIP file: {str(e)}"}), 500

        # Handles invalid data inputs
        else:
            return jsonify({"error": "Invalid request format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get-file-results", methods=["GET"])
def get_file_results():
    filename = request.args.get('filename')
    if not filename:
        return jsonify({'error': 'Please include a file name'}), 400

    results = analyzer.get_file_results(filename)

    if not results:
        return jsonify({'error': 'File results do not exist'}), 404

    return jsonify(results), 200

if __name__ == "__main__":
    app.run(debug=True)

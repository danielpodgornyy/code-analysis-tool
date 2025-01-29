import os
import tempfile
import zipfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from git import Repo, exc
from criteria.line_length import LineLengthCriterion
from config import CRITERIA

app = Flask(__name__)
CORS(app, origins=["http://localhost:4200"])

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

# Error: "An error occurred while extracting the ZIP file: expected str, bytes or os.PathLike object, not TextIOWrapper"
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
                    results[file_path][criterion_name] = checker.analyze(absolute_path) # Pass the path
    return results

@app.route("/run-analyzer", methods=["POST"])
def run_analyzer():
    """Handles both Git repo analysis and local file uploads."""
    try:
        if request.is_json:
            data = request.get_json()
            repo_url = data.get("repo_url")

            if not repo_url:
                return jsonify({"error": "No repository URL provided"}), 400

            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"Cloning repository from {repo_url} into {temp_dir}...")

                try:
                    repo = Repo.clone_from(repo_url, temp_dir)

                    if repo.bare:
                        return jsonify({"error": "The repository is bare or invalid."}), 400

                    repo.git.checkout()
                    directory = temp_dir

                    file_list = list_files_from_directory(directory)
                    if not file_list:
                        return jsonify({"error": "No files found in the repository."}), 400

                    analysis_results = analyze_files(directory, file_list)

                    return jsonify({"files": file_list, "analysis": analysis_results}), 200

                except exc.GitCommandError as e:
                    return jsonify({"error": f"Failed to clone repository: {e.stderr.strip()}"}), 500

        # Error: "An error occurred while extracting the ZIP file: expected str, bytes or os.PathLike object, not TextIOWrapper"
        elif 'file' in request.files:
            uploaded_file = request.files['file']

            if not uploaded_file.filename.endswith('.zip'):
                return jsonify({"error": "Only .zip files are allowed"}), 400

            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = os.path.join(temp_dir, uploaded_file.filename)
                uploaded_file.save(zip_path)

                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)

                    # After extracting, check if all files inside are properly encoded
                    file_list = list_files_from_directory(temp_dir)
                    if not file_list:
                        return jsonify({"error": "No files found in the uploaded ZIP."}), 400

                    analysis_results = analyze_files(temp_dir, file_list)

                    return jsonify({"files": file_list, "analysis": analysis_results}), 200

                except zipfile.BadZipFile:
                    return jsonify({"error": "The uploaded file is not a valid ZIP file."}), 400
                except Exception as e:
                    return jsonify({"error": f"An error occurred while extracting the ZIP file: {str(e)}"}), 500

        else:
            return jsonify({"error": "Invalid request format"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

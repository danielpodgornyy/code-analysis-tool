# The input is using command line only (not connected to Flask/Angular)

import os
import tempfile
from git import Repo, exc
from criteria.line_length import LineLengthCriterion
from config import CRITERIA
from criteria.class_Extractor import ClassExtractor


def list_files_from_directory(directory):
    """List all files in a directory, excluding hidden ones."""
    file_list = []
    for root, dirs, files in os.walk(directory):
        # Remove hidden directories (like .git) from traversal
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if not file.startswith('.'):  # Skip hidden files
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                file_list.append(relative_path)
    return file_list


def display_file_contents(directory, file_list):
    """Display the contents of each file in the list."""
    print("\nFile Contents:")
    for relative_path in file_list:
        absolute_path = os.path.join(directory, relative_path)
        print(f"\n--- Reading {absolute_path} ---")
        try:
            with open(absolute_path, 'r', encoding='utf-8') as file:
                print(file.read())
        except Exception as e:
            print(f"Error reading {absolute_path}: {e}")


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
                    results[file_path][criterion_name] = checker.analyze(absolute_path)  # Pass the path

                elif criterion_name == "class_extraction":
                    extractor = ClassExtractor()
                    results[file_path][criterion_name] = extractor.analyze(absolute_path)  # Pass the path

        results[file_path]["summary"] = {key: val for key, val in results[file_path].items()}

    return results


def list_display_and_analyze_files(repo_url_or_path):
    """List, display, and analyze files from a local directory or Git repository."""
    if os.path.isdir(repo_url_or_path):
        # Use the local directory
        directory = repo_url_or_path
    else:
        # Clone the Git repository to a temporary directory
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"Cloning repository from {repo_url_or_path} into {temp_dir}...")
                repo = Repo.clone_from(repo_url_or_path, temp_dir)

                # Ensure files are checked out properly
                if repo.bare:
                    raise Exception("The repository is bare or invalid.")
                repo.git.checkout()

                directory = temp_dir

                # Ensure repository contains files after cloning
                file_list = list_files_from_directory(directory)
                if not file_list:
                    print("No files found in the repository after cloning.")
                    return
                print("\nRepository Files (excluding hidden files):")
                for file in file_list:
                    print(file)

                # Now that the files are accessible, display file contents and analyze them
                display_file_contents(directory, file_list)

                # Analyze files
                print("\nAnalyzing Files:")
                analysis_results = analyze_files(directory, file_list)
                for file, issues in analysis_results.items():
                    print(f"\n--- {file} ---")
                    for criterion, violations in issues.items():
                        if violations:
                            print(f"\n{criterion.capitalize()} Violations:")
                            print("\n".join(violations))
                        else:
                            print(f"{criterion.capitalize()}: No violations found.")

        except exc.GitCommandError as e:
            raise Exception(f"Failed to clone repository. Error: {e.stderr.strip()}") from e


# Main program
if __name__ == "__main__":
    repo_url_or_path = input("Enter the Git repository URL or local directory path: ").strip()
    if repo_url_or_path:
        try:
            list_display_and_analyze_files(repo_url_or_path)
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("No URL or path entered. Exiting...")

# Testing line for line lenght: zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz

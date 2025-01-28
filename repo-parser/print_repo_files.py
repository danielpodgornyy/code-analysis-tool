import os
import tempfile
from git import Repo, exc

def list_and_print_file_contents_from_directory(directory):
    # List all files first
    print("\nParsing files from local directory:")
    print("\nRepository Files (excluding hidden files):")
    file_list = []  # To store file paths for later use
    for root, dirs, files in os.walk(directory):
        # Remove hidden directories (like .git) from traversal
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if not file.startswith('.'):  # Skip hidden files
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                file_list.append(relative_path)
                print(relative_path)  # List file names

    # Print the contents of each file
    print("\nFile Contents:")
    for relative_path in file_list:
        file_path = os.path.join(directory, relative_path)
        print(f"\n--- Contents of {relative_path} ---")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                print(f.read())
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

def list_and_print_file_contents(repo_url_or_path):
    # Determine whether the input is a local directory or a Git URL
    if os.path.isdir(repo_url_or_path):
        # Use the local directory
        list_and_print_file_contents_from_directory(repo_url_or_path)
    else:
        try:
            # Assume it's a Git URL and clone the repository
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"Cloning repository from {repo_url_or_path} into {temp_dir}...")
                repo = Repo.clone_from(repo_url_or_path, temp_dir)
                
                # Check if the repo is valid
                if repo.bare:
                    raise Exception("The repository is bare or invalid.")

                list_and_print_file_contents_from_directory(temp_dir)
        except exc.GitCommandError as e:
            raise Exception(f"Failed to clone repository. Error: {e.stderr.strip()}") from e

# Main program
if __name__ == "__main__":
    repo_url_or_path = input("Enter the Git repository URL or local directory path: ").strip()
    if repo_url_or_path:
        try:
            list_and_print_file_contents(repo_url_or_path)
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("No URL or path entered. Exiting...")

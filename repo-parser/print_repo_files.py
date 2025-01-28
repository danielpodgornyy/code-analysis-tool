import os
import tempfile
from git import Repo

def list_and_print_file_contents(repo_url):
    # Create a temporary directory to clone the repository
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Cloning repository from {repo_url} into {temp_dir}...")
        repo = Repo.clone_from(repo_url, temp_dir)
        
        # Check if the repo is valid
        if repo.bare:
            raise Exception("The repository is bare or invalid.")

        # List all files first
        print("\nRepository Files (excluding hidden files):")
        file_list = []  # To store file paths for later use
        for root, dirs, files in os.walk(temp_dir):
            # Remove hidden directories (like .git) from traversal
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if not file.startswith('.'):  # Skip hidden files
                    relative_path = os.path.relpath(os.path.join(root, file), temp_dir)
                    file_list.append(relative_path)
                    print(relative_path)  # List file names

        # Print the contents of each file
        print("\nFile Contents:")
        for relative_path in file_list:
            file_path = os.path.join(temp_dir, relative_path)
            print(f"\n--- Contents of {relative_path} ---")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    print(f.read())
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

# Test the function
repo_url = "https://github.com/rtyley/small-test-repo"
list_and_print_file_contents(repo_url)

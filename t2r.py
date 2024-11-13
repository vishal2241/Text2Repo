import os
import argparse

def parse_repo_text(file_path):
    """
    Parse the structured text file to reconstruct the repository.
    
    Args:
        file_path (str): The path to the input text file containing the repository structure.

    Returns:
        list: A list of tuples where each tuple is (relative_path, content) of a file.
    """
    file_contents = []
    current_path = ""
    current_content = []
    in_file_content = False

    with open(file_path, 'r') as f:
        for line in f:
            stripped_line = line.strip()

            # Check for directory/file tree markers
            if stripped_line == "<-- Directory/File Tree Ends":
                continue
            if stripped_line == "File Content Begin -->":
                in_file_content = True
                continue

            if not in_file_content:
                # Parse directory structure
                if stripped_line.endswith('/'):
                    current_path = stripped_line[:-1]
                    os.makedirs(current_path, exist_ok=True)
                elif stripped_line:
                    # Parse files in directory tree
                    file_path = os.path.join(current_path, stripped_line)
                    open(file_path, 'a').close()  # Create empty file
            else:
                # Parse file contents section
                if stripped_line.startswith("[File Begins]"):
                    if current_content:
                        file_contents.append((current_file_path, "".join(current_content)))
                        current_content = []
                    current_file_path = stripped_line[len("[File Begins] "):]
                elif stripped_line.startswith("[File Ends]"):
                    file_contents.append((current_file_path, "".join(current_content)))
                    current_content = []
                else:
                    # Collect file content
                    current_content.append(line)

    return file_contents

def write_files(file_contents):
    """
    Write the content to each file in the repository.

    Args:
        file_contents (list): A list of tuples where each tuple is (relative_path, content) of a file.
    """
    for file_path, content in file_contents:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)

def main():
    parser = argparse.ArgumentParser(description='Reconstruct a repository from a text file generated by repo2txt.')
    parser.add_argument('input_file', help='The input text file with the repository structure and contents.')
    args = parser.parse_args()

    file_contents = parse_repo_text(args.input_file)
    write_files(file_contents)

if __name__ == "__main__":
    main()

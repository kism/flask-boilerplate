#! /usr/bin/env python3
"""Create new project in parent directory with your your defined name."""

# Imports, for this script NO external packages should be required.

import os
import re
import shutil
import sys

# region: Get new app related names

if len(sys.argv) > 1:  # USE QUOTES IF YOU ARE USING THE PROGRAM LIKE THIS
    new_project_name_prompt = sys.argv[1]
else:
    print("Enter the name of the app, with spaces between each word.")
    print("For example: my dank app")
    new_project_name_prompt = input("Name: ")

new_project_name_split = new_project_name_prompt.split()

while len(new_project_name_split) == 1:
    print("Please make the project name more than one word.")
    new_project_name_prompt = input("Name: ")
    new_project_name_split = new_project_name_prompt.split()

new_name = ("".join(new_project_name_split)).lower()
new_name_camel_case = "".join(x for x in new_project_name_prompt.title() if not x.isspace())
new_config_var = "".join([word[0] for word in new_project_name_split]) + "_conf"

print(f"new_name: {new_name}")
print(f"new_name_camel_case: {new_name_camel_case}")
print(f"new_config_var: {new_config_var}")

# endregion
# region: Create new app folder

parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
dest_folder_path = os.path.join(parent_dir, new_name)

if os.path.exists(dest_folder_path):  # Check if the folder already exists
    print(f"The folder '{new_name}' already exists in parent directory, exiting.")
    sys.exit(1)
else:
    # Create the folder
    os.makedirs(dest_folder_path)
    print(f"The folder '{new_name}' has been created in the parent directory.")

# endregion
# region: Copy folders to destination

to_copy_folder_list = [".github", ".vscode", "mycoolapp", "tests"]

for folder_name in to_copy_folder_list:
    shutil.copytree(os.path.join(os.getcwd(), folder_name), os.path.join(dest_folder_path, folder_name))

to_copy_file_list = ["pyproject.toml", "poetry.toml", ".gitignore"]
for file_name in to_copy_file_list:
    shutil.copyfile(os.path.join(os.getcwd(), file_name), os.path.join(dest_folder_path, file_name))

shutil.copyfile(os.path.join(os.getcwd(), "README_NEWREPO.md"), os.path.join( dest_folder_path, "README.md"))

# endregion
# region: Remove unwanted dirs
folders_to_remove = ["__pycache__"]

for root, dirs, _ in os.walk(dest_folder_path, topdown=False):
    for name in dirs:
        if name in folders_to_remove:
            folder_path = os.path.join(root, name)
            shutil.rmtree(folder_path)


# endregion
# region: Replace strings in files


def find_and_replace_in_files(directory: str, find_str: str, replace_str: str) -> None:
    """Recursively replace strings in files."""
    for root, __, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
            new_content = content.replace(find_str, replace_str)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)


find_and_replace_in_files(dest_folder_path, "mycoolapp", new_name)
find_and_replace_in_files(dest_folder_path, "MyCoolApp", new_name_camel_case)
find_and_replace_in_files(dest_folder_path, "mca_conf", new_config_var)


# endregion
# region: Replace file and dir names


def find_and_replace_file_names(directory: str, find_str: str, replace_str: str) -> None:
    """Recursively replace strings in files."""
    for root, _, files in os.walk(directory):
        for file_name in files:
            if find_str in file_name:
                old_path = os.path.join(root, file_name)
                new_path = os.path.join(root, file_name.replace(find_str, replace_str))
                os.rename(old_path, new_path)


def find_and_replace_dir_names(directory: str, find_str: str, replace_str: str) -> None:
    """Recursively replace strings in dirs."""
    for dirpath, dirnames, _ in os.walk(directory):
        for dirname in dirnames:
            if find_str in dirname:
                old_path = os.path.join(dirpath, dirname)
                new_path = os.path.join(dirpath, dirname.replace(find_str, replace_str))
                os.rename(old_path, new_path)


def find_and_replace_file_dir_names(directory: str, find_str: str, replace_str: str) -> None:
    """Do both."""
    find_and_replace_dir_names(directory, find_str, replace_str)
    find_and_replace_file_names(directory, find_str, replace_str)


find_and_replace_file_dir_names(dest_folder_path, "mycoolapp", new_name)

# endregion
# region: Edit pyproject.toml, .github/workflows/main.yml


def remove_text(file_path: str, pattern: str) -> None:
    """Remove text from file per compiled regex pattern."""
    # Read the file content
    with open(file_path) as file:
        content = file.read()

    # Use re.DOTALL to include newline characters in the match
    modified_content = re.sub(pattern, "", content)

    # Write the modified content back to the file
    with open(file_path, "w") as file:
        file.write(modified_content)


# endregion
# region: Path to the file you want to modify
file_path = os.path.join(dest_folder_path, "pyproject.toml")
pattern = re.compile(r"\"create_my_new_project\.py\".*?\]", re.DOTALL)
remove_text(file_path, pattern)

file_path = os.path.join(dest_folder_path, ".github", "workflows", "test.yml")
pattern = re.compile("^.*Upload coverage reports to Codecov" + ".*\n")
remove_text(file_path, pattern)

file_path = os.path.join(dest_folder_path, ".gitignore")
pattern = re.compile(re.escape("# Only for the boilerplate") + ".*\n")
remove_text(file_path, pattern)
pattern = re.compile(re.escape("poetry.lock") + ".*\n")
remove_text(file_path, pattern)


# endregion
# region: Print instructions
print(f"""
Done!

Todo for you, get the css:
---------------------------------
cd {dest_folder_path}
cd {new_name}
curl -LsS https://github.com/kism/zy.css/releases/download/main/grab.sh | bash
cd ..
---------------------------------
Todo for you: Read your new projects README.md for the next steps.
""")
# endregion

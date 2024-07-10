#! /usr/bin/env python3
"""Create new project in parent directory with your your defined name."""

# Imports, for this script NO external packages should be required.

import os
import shutil
import sys

# Get new app related names

if sys.argv[1]:  # USE QUOTES IF YOU ARE USING THE PROGRAM LIKE THIS
    new_project_name_prompt = sys.argv[1]
else:
    print("Enter the name of the app, with spaces between each word.")
    print("For example: My Dank App")
    new_project_name_prompt = input("Name: ")

new_project_name_split = new_project_name_prompt.split()

new_name = ("".join(new_project_name_split)).lower()
new_name_camel_case = "".join(x for x in new_project_name_prompt.title() if not x.isspace())
new_settings_var = "".join([word[0] for word in new_project_name_split]) + "_sett"

print(f"new_name: {new_name}")
print(f"new_name_camel_case: {new_name_camel_case}")
print(f"new_settings_var: {new_settings_var}")

# Create new app folder

parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
dest_folder_path = os.path.join(parent_dir, new_name)

if os.path.exists(dest_folder_path):  # Check if the folder already exists
    print(f"The folder '{new_name}' already exists in parent directory, exiting.")
    sys.exit(1)
else:
    # Create the folder
    os.makedirs(dest_folder_path)
    print(f"The folder '{new_name}' has been created in the parent directory.")

# Copy folders to destination

to_copy_folder_list = [".github", ".vscode", "mycoolapp", "tests"]

for folder_name in to_copy_folder_list:
    shutil.copytree(os.getcwd() + os.sep + folder_name, dest_folder_path + os.sep + folder_name)

to_copy_file_list = ["pyproject.toml", "poetry.toml", ".gitignore"]
for file_name in to_copy_file_list:
    shutil.copyfile(os.getcwd() + os.sep + file_name, dest_folder_path + os.sep + file_name)

shutil.copyfile(os.getcwd() + os.sep + "README_NEWREPO.md", dest_folder_path + os.sep + "README.md")

# Remove unwanted dirs
folders_to_remove = ["__pycache__"]

for root, dirs, _ in os.walk(dest_folder_path, topdown=False):
    for name in dirs:
        if name in folders_to_remove:
            folder_path = os.path.join(root, name)
            shutil.rmtree(folder_path)
            print(f"Removed: {folder_path}")


# Replace strings in files


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
            print(f"Replaced string in: {file_path}")


find_and_replace_in_files(dest_folder_path, "mycoolapp", new_name)
find_and_replace_in_files(dest_folder_path, "MyCoolApp", new_name_camel_case)
find_and_replace_in_files(dest_folder_path, "mca_sett", new_settings_var)


# Replace file and dir names


def find_and_replace_file_names(directory: str, find_str: str, replace_str: str) -> None:
    """Recursively replace strings in files."""
    for root, _, files in os.walk(directory):
        for file_name in files:
            if find_str in file_name:
                old_path = os.path.join(root, file_name)
                new_path = os.path.join(root, file_name.replace(find_str, replace_str))
                os.rename(old_path, new_path)
                print(f"Renamed file: {old_path} to {new_path}")


def find_and_replace_dir_names(directory: str, find_str: str, replace_str: str) -> None:
    """Recursively replace strings in dirs."""
    for dirpath, dirnames, _ in os.walk(directory):
        for dirname in dirnames:
            if find_str in dirname:
                old_path = os.path.join(dirpath, dirname)
                new_path = os.path.join(dirpath, dirname.replace(find_str, replace_str))
                os.rename(old_path, new_path)
                print(f"Renamed directory: {old_path} -> {new_path}")


def find_and_replace_file_dir_names(directory: str, find_str: str, replace_str: str) -> None:
    """Do both."""
    find_and_replace_dir_names(directory, find_str, replace_str)
    find_and_replace_file_names(directory, find_str, replace_str)


find_and_replace_file_dir_names(dest_folder_path, "mycoolapp", new_name)

print("Done!")

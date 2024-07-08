"""This is code that runs before any pytest tests are actually run."""

import os
import shutil

TEST_INSTANCE_PATH = f"{os.getcwd()}{os.sep}instance_test"

# Cleanup TEST_INSTANCE_PATH directory
if os.path.exists(TEST_INSTANCE_PATH):
    shutil.rmtree(TEST_INSTANCE_PATH)

# Recreate the folder
os.makedirs(TEST_INSTANCE_PATH)

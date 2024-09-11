import re
import sys

MODULE_REGEX = r"^[\-'a-zA-Z ]+$"
app_slug = "{{ cookiecutter.app_slug }}"

if not re.match(MODULE_REGEX, app_slug):
    print(f"ERROR: {app_slug} is not a valid Python module name!")
    sys.exit(1)

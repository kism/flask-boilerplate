import re
import sys

print()
print("--- Validating inputs ---")

print("Template variables:")
print("  __app_nice_name: {{ cookiecutter.__app_nice_name }}")
print("  __app_slug: {{ cookiecutter.__app_slug }}")
print("  __app_package: {{ cookiecutter.__app_package }}")
print("  __app_camel_case: {{ cookiecutter.__app_camel_case }}")
print("  __app_config_var: {{ cookiecutter.__app_config_var }}")

MODULE_REGEX = r"^[\-'a-zA-Z ]+$"
__app_package = "{{ cookiecutter.__app_package }}"
__app_nice_name = "{{ cookiecutter.__app_nice_name }}"

if not re.match(MODULE_REGEX, __app_package):
    print(f"ERROR: {__app_package} is not a valid Python module name!")
    sys.exit(1)

if len(__app_nice_name.split()) < 2:
    print("ERROR: App name should not be a single word!")
    sys.exit(1)

print()
print("Done validating inputs, generating project...")

import os
import sys


def setup_path():
    # Get pyton scripts directory
    python_base_path = os.path.dirname(sys.executable)

    # Check if base path is in the Scripts directory
    if os.path.basename(os.path.normpath(python_base_path)) != "Scripts":
        scripts_dir = os.path.join(python_base_path, "Scripts")
    else:
        scripts_dir = python_base_path

    # Add scripts directory to PATH if not already there
    if not os.path.exists(scripts_dir):
        raise SystemError(f"Scripts directory not found in {python_base_path}")

    # Add to path if not already there
    if scripts_dir not in os.environ["PATH"].split(os.pathsep):
        # Add the Scripts directory to the PATH
        os.environ["PATH"] += os.pathsep + scripts_dir
        print("Warn: Python/Scripts directory was not in PATH, added it.")

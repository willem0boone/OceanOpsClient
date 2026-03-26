"""
This is the docstring for the harvest_plet module.
"""

import os
import json
from .OceanOpsClient import OceanOpsClient
__all__ = ["OceanOpsClient"]


def extract_version_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data.get('version', 'Version not found')
    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found."
    except json.JSONDecodeError:
        return "Error: The file could not be decoded as JSON."
    except Exception as e:
        return f"An unexpected error occurred: {e}"


# Get the path relative to this __init__.py file
codemeta_path = os.path.join(os.path.dirname(__file__), "..", "codemeta.json")
__version__ = extract_version_from_file(codemeta_path)

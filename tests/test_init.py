import sys
import os

# Add project root to Python path so tests can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import OceanOpsClient

print("Version:", OceanOpsClient.__version__)
client = OceanOpsClient.OceanOpsClient()
print("Client loaded:", client)

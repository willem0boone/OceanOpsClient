import sys
import os
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import OceanOpsClient


def test_import_and_version():
    assert re.fullmatch(r"\d+\.\d+\.\d+", OceanOpsClient.__version__)
    client = OceanOpsClient.OceanOpsClient()
    assert client is not None


if __name__ == "__main__":
    test_import_and_version()


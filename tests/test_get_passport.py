import unittest
from OceanOpsClient.OceanOpsClient import OceanOps


class TestGetPlatform(unittest.TestCase):
    def setUp(self):
        # Initialize the client (read-only mode)
        self.client = OceanOps()
        # Example WIGOS ID known to exist in the API
        self.wigosID = "0-22000-0-6204817"

    def test_get_platform_returns_data(self):
        """
        Test that get_platform returns a dict with 'data' and 'total',
        and that 'data' contains at least one platform object.
        """
        resp = self.client.get_platform(ptfWigosId=self.wigosID)

        # Verify response structure
        self.assertIsInstance(resp, dict)
        self.assertIn("data", resp)
        self.assertIn("total", resp)

        # There should be at least one platform
        self.assertGreaterEqual(resp["total"], 1)
        self.assertGreaterEqual(len(resp["data"]), 1)

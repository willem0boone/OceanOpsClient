"""Live integration tests for OceanOpsClient passport lookup methods.

These tests make real OceanOPS API requests and are skipped unless
OCEANOPS_LIVE_TESTS=1 is set in the environment.
"""

import os
import unittest

from OceanOpsClient import OceanOpsClient


WIGOS_ID = "0-22000-0-6204817"
INTERNAL_ID = "007"
PROGRAM_ID = "1006434"
PLF_ID = 1305758
OCEANOPS_LIVE_TESTS = "0"

@unittest.skipUnless(
    OCEANOPS_LIVE_TESTS == "1",
    "Set OCEANOPS_LIVE_TESTS=1 to run live API tests.",
)
class TestGetPassportLive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = OceanOpsClient()

    def _assert_live_response(self, response):
        self.assertIsInstance(response, dict)
        self.assertIn("total", response)
        self.assertGreaterEqual(response["total"], 0)
        self.assertTrue(
            "data" in response or "items" in response,
            "Expected a result list under 'data' or 'items'.",
        )
        results = response.get("data", response.get("items", []))
        self.assertIsInstance(results, list)
        self.assertGreaterEqual(len(results), 1)

    def test_get_by_wigos_id_live(self):
        response = self.client.get_by_wigosID(ptfWigosId=WIGOS_ID)
        self._assert_live_response(response)

    def test_get_by_internal_id_live(self):
        response = self.client.get_by_internalID(internal_id=INTERNAL_ID, program=PROGRAM_ID)
        self._assert_live_response(response)

    def test_get_by_plf_id_live(self):
        response = self.client.get_by_plfID(plf_id=PLF_ID, program=PROGRAM_ID)
        self._assert_live_response(response)


if __name__ == "__main__":
    unittest.main()

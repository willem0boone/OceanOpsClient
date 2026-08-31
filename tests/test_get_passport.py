"""Tests for OceanOpsClient passport lookup methods and alias behavior.
Tthese tests are not hitting the OceanOPS API. They only verify:
- the method builds the right URL/payload
- raise_for_status() / json() are handled
- the alias get_platform still routes correctly"""

import unittest
from unittest.mock import Mock
from unittest.mock import patch

from OceanOpsClient import OceanOpsClient


WIGOS_ID = "0-22000-0-6204817"
INTERNAL_ID = "007"
PROGRAM_ID = "1006434"
PLF_ID = 1305758


class TestGetPassport(unittest.TestCase):
    def setUp(self):
        self.client = OceanOpsClient()

    @patch("OceanOpsClient.OceanOpsClient.requests.get")
    def test_get_by_wigos_id_returns_data(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"data": [{"id": 1305758}], "total": 1}
        mock_get.return_value = mock_response

        resp = self.client.get_by_wigosID(ptfWigosId=WIGOS_ID)

        self.assertEqual(resp["total"], 1)
        mock_get.assert_called_once_with(
            f"https://www.ocean-ops.org/api/data/platform/wigosid/{WIGOS_ID}"
        )

    @patch("OceanOpsClient.OceanOpsClient.requests.post")
    def test_get_by_internal_id_posts_expected_payload(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"data": [{"id": 1305758}], "total": 1}
        mock_post.return_value = mock_response

        resp = self.client.get_by_internalID(INTERNAL_ID, program=PROGRAM_ID)

        self.assertEqual(resp["total"], 1)
        mock_post.assert_called_once_with(
            "https://www.ocean-ops.org/api/data/passports/search",
            json={
                "internalIds": [INTERNAL_ID],
                "filters": {"programs": PROGRAM_ID},
            },
            timeout=30,
        )

    @patch("OceanOpsClient.OceanOpsClient.requests.post")
    def test_get_by_plf_id_posts_expected_payload(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"data": [{"id": 1305758}], "total": 1}
        mock_post.return_value = mock_response

        resp = self.client.get_by_plfID(PLF_ID, program=PROGRAM_ID)

        self.assertEqual(resp["total"], 1)
        mock_post.assert_called_once_with(
            "https://www.ocean-ops.org/api/data/passports/search",
            json={
                "ptfIds": [PLF_ID],
                "filters": {"programs": PROGRAM_ID},
            },
            timeout=30,
        )

    @patch("OceanOpsClient.OceanOpsClient.requests.get")
    def test_get_platform_remains_alias(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"data": [{"id": 1305758}], "total": 1}
        mock_get.return_value = mock_response

        resp = self.client.get_platform(ptfWigosId=WIGOS_ID)

        self.assertEqual(resp["total"], 1)
        mock_get.assert_called_once()


if __name__ == "__main__":
    unittest.main()

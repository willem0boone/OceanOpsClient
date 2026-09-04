import tempfile
import unittest
from pathlib import Path
from unittest import mock
from OceanOpsClient import OceanOpsClient


class TestOceanOps(unittest.TestCase):
    def setUp(self):
        # Environment values we'll inject in tests
        self.env = {
            "API_KEY_ID": "fake-id",
            "API_KEY_TOKEN": "fake-token",
        }

    def test_from_env(self):
        with mock.patch.dict("os.environ", self.env, clear=False):
            client = OceanOpsClient.from_env()
            self.assertEqual(client.settings.API_KEY_ID, "fake-id")
            self.assertEqual(client.settings.API_KEY_TOKEN.get_secret_value(), "fake-token")

    def test_from_credentials(self):
        client = OceanOpsClient.from_credentials("fake-id", "fake-token")
        self.assertEqual(client.settings.API_KEY_ID, "fake-id")
        self.assertEqual(client.settings.API_KEY_TOKEN.get_secret_value(), "fake-token")

    def test_from_env_with_unrelated_variables(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            env_path = Path(tmp_dir) / ".env"
            env_path.write_text(
                "API_KEY_ID = \"1642\"\n"
                "API_KEY_TOKEN = \"P4vt6t-jDe59TdOlbUtPNEXHE9g\"\n"
                "ETN_USER = \"willem.boone@vliz.be\"\n"
                "ETN_PWD = \"pkYUsHCcz4d\"\n",
                encoding="utf-8",
            )

            client = OceanOpsClient.from_env(str(env_path))
            self.assertEqual(client.settings.API_KEY_ID, "1642")
            self.assertEqual(
                client.settings.API_KEY_TOKEN.get_secret_value(),
                "P4vt6t-jDe59TdOlbUtPNEXHE9g",
            )

    def test_init_without_settings(self):
        client = OceanOpsClient()
        self.assertIsNone(client.settings)

    def test_post_get_id_rejects_tuple_values(self):
        client = OceanOpsClient.from_credentials("fake-id", "fake-token")

        with self.assertRaisesRegex(TypeError, "Remove any trailing comma"):
            client.post_get_id(
                program=("vliz-arms-mbon",),
                start_date="2026-06-15T12:00:00",
                longitude=(4.6,),
                latitude=(51.2,),
            )

    def test_post_get_id_requires_full_iso_datetime(self):
        client = OceanOpsClient.from_credentials("fake-id", "fake-token")

        with self.assertRaisesRegex(ValueError, "full ISO datetime"):
            client.post_get_id(
                program="vliz-arms-mbon",
                start_date="2026-06-15T12:00",
                longitude=4.6,
                latitude=51.2,
            )



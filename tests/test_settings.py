import unittest
from pathlib import Path
from OceanOpsClient.OceanOpsClient import OceanOps


class TestOceanOps(unittest.TestCase):
    def test_from_env(self):
        client = OceanOps.from_env()
        self.assertIsNotNone(client.settings.API_KEY_ID)
        self.assertIsNotNone(client.settings.API_KEY_TOKEN)

    def test_from_cli(self):
        env_path = Path(__file__).parent / ".env"
        client = OceanOps.from_env(env_path)
        self.assertIsNotNone(client.settings.API_KEY_ID)
        self.assertIsNotNone(client.settings.API_KEY_TOKEN)

    def test_init_without_settings(self):
        client = OceanOps()
        self.assertIsNone(client.headers)



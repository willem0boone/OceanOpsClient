import unittest
from pathlib import Path
from OceanOpsClient.OceanOpsClient import OceanOps


class TestValidatePassport(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = OceanOps()  # no credentials needed for validation
        cls.test_json_path = Path(__file__).parent / "sources" / "test_passport.json"

    def test_validate_with_online_schema(self):
        """
        Test validation using the official online schema.
        Note: will fail if JSON uses unsupported fields like wigosId.
        """
        if not self.test_json_path.exists():
            self.skipTest(f"Missing test JSON: {self.test_json_path}")

        try:
            result = self.client.validate_passport_json(
                self.test_json_path,
                use_local_schema=False
            )
            self.assertTrue(result)
        except Exception as e:
            self.fail(f"Validation with online schema failed: {e}")

    def test_validate_with_local_schema(self):
        """
        Test validation using local schema (supports extensions like wigosId).
        """
        if not self.test_json_path.exists():
            self.skipTest(f"Missing test JSON: {self.test_json_path}")

        try:
            result = self.client.validate_passport_json(
                self.test_json_path,
                use_local_schema=True
            )
            self.assertTrue(result)
        except Exception as e:
            self.fail(f"Validation with local schema failed: {e}")

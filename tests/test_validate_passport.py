import unittest
from pathlib import Path
from OceanOpsClient.OceanOpsClient import OceanOps


class TestValidatePassport(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = OceanOps()  # no credentials needed for validation
        cls.test_json_path = Path(__file__).parent / "sources" / "test_passport.json"
        cls.local_schema_path = Path(__file__).parent / "sources" / "local_schema.json"

    # def test_validate_with_online_schema(self):
    #     """
    #     Test validation using the official online schema.
    #     Note: will fail if JSON uses unsupported fields like wigosId.
    #     """
    #     if not self.test_json_path.exists():
    #         self.skipTest(f"Missing test JSON: {self.test_json_path}")
    #
    #     try:
    #         result = self.client.validate_passport_json(
    #             self.test_json_path
    #             # no schema_source → defaults to online schema
    #         )
    #         self.assertTrue(result)
    #     except Exception as e:
    #         self.fail(f"Validation with online schema failed: {e}")

    def test_validate_with_local_schema(self):
        """
        Test validation using a user-provided local schema (supports extensions like wigosId).
        """
        if not self.test_json_path.exists():
            self.skipTest(f"Missing test JSON: {self.test_json_path}")
        if not self.local_schema_path.exists():
            self.skipTest(f"Missing local schema JSON: {self.local_schema_path}")

        try:
            result = self.client.validate_passport_json(
                self.test_json_path,
                schema_source=self.local_schema_path
            )
            self.assertTrue(result)
        except Exception as e:
            self.fail(f"Validation with local schema failed: {e}")


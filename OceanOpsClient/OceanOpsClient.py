import json
from urllib.request import urlopen, Request
from OceanOpsClient.config import Settings

PASSPORT_TEMPLATE = (
    "https://www.ocean-ops.org/passports/examples/a-input-passport.json"
)


class OceanOps:
    BASE_URL = "https://www.ocean-ops.org/api/data"

    def __init__(self, settings: Settings):
        self.settings = settings

        self.headers = {
            "Content-Type": "application/json",
            "X-OceanOPS-Metadata-ID": settings.API_KEY_ID,
            "X-OceanOPS-Metadata-Token":
                settings.API_KEY_TOKEN.get_secret_value(),
        }

    @classmethod
    def from_env(cls):
        """
        Load credentials from environment / .env / CLI via Settings
        """
        return cls(Settings())

    @classmethod
    def from_credentials(cls, key_id: str, token: str):
        """
        Manually pass credentials (highest priority)
        """
        return cls(Settings(API_KEY_ID=key_id, API_KEY_TOKEN=token))

    @property
    def get_id_url(self):
        return f"{self.BASE_URL}/platforms/getid"

    def push_passport(self):
        pass



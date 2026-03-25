import json
import requests
from typing import Any, Dict, Union, Optional
from pathlib import Path
from jsonschema import validate
from OceanOpsClient.config import Settings


class OceanOps:
    """
    Client for interacting with the OceanOPS API.

    Provides methods for read-only data retrieval and authenticated
    data submission. Supports JSON schema validation of OceanOPS
    "passport" files.

    Attributes:
        BASE_URL (str): Base URL for OceanOPS API endpoints. :noindex:
        DEFAULT_SCHEMA_URL (str): URL to the default passport JSON schema. :noindex:
        LOCAL_SCHEMA_PATH (Path): Local path to the JSON schema file. :noindex:
        settings (Optional[Settings]): Optional credentials/settings.
        headers (Optional[Dict[str, str]]): HTTP headers for authenticated
            requests. None if no credentials provided.
    """

    BASE_URL = "https://www.ocean-ops.org/api/data"
    DEFAULT_SCHEMA_URL = (
        "https://www.ocean-ops.org/passports/examples/a-passport-input.schema.json"
    )
    LOCAL_SCHEMA_PATH = Path(__file__).parent / "passport_schema" / "local_schema.json"

    def __init__(self, settings: Optional["Settings"] = None) -> None:
        """
        Initialize an OceanOps client.

        Args:
            settings (Optional[Settings]): Optional credentials/settings.
                If None, client operates in read-only mode.
        """
        self.settings = settings

        if self.settings:
            self.headers = {
                "Content-Type": "application/json",
                "X-OceanOPS-Metadata-ID": self.settings.API_KEY_ID,
                "X-OceanOPS-Metadata-Token": self.settings.API_KEY_TOKEN.get_secret_value(),
            }
        else:
            self.headers = None  # read-only mode

    @classmethod
    def from_env(cls, env_file: Optional[str] = None) -> "OceanOps":
        """
        Create an OceanOps client from environment variables or a .env file.

        Args:
            env_file (Optional[str]): Path to a .env file. If None, uses
                default environment variables.

        Returns:
            OceanOps: Instance of OceanOps client. If credentials cannot
                be loaded, returns a read-only client.
        """
        try:
            settings = Settings(_env_file=env_file) if env_file else Settings()
            return cls(settings)
        except Exception:
            # Failed to load credentials → return read-only client
            return cls(None)

    @classmethod
    def from_credentials(cls, key_id: str, token: str) -> "OceanOps":
        """
        Create an OceanOps client from explicit credentials.

        Args:
            key_id (str): API key ID.
            token (str): API key token.

        Returns:
            OceanOps: Instance of OceanOps client with credentials.
        """
        settings = Settings(API_KEY_ID=key_id, API_KEY_TOKEN=token)
        return cls(settings)

    def get_platform(self, ptfWigosId: str) -> Dict[str, Any]:
        """
        Retrieve platform information from OceanOPS using a WIGOS ID.

        Args:
            ptfWigosId (str): Platform WIGOS ID.

        Returns:
            Dict[str, Any]: JSON response from the OceanOPS API.

        Raises:
            ValueError: If ptfWigosId is not provided.
            requests.HTTPError: If the API request fails.
        """
        if not ptfWigosId:
            raise ValueError("ptfWigosId must be provided")

        url = f"{self.BASE_URL}/platform/wigosid/{ptfWigosId}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def push_data(self, payload: Dict[str, Any]) -> Dict[str, str]:
        """
        Push data to OceanOPS. Requires authenticated client.

        Args:
            payload (Dict[str, Any]): Data to push to the API.

        Returns:
            Dict[str, str]: Status of the operation.

        Raises:
            RuntimeError: If client does not have credentials.
        """
        if not self.headers:
            raise RuntimeError("Cannot push data: credentials required")
        # TODO: Implement actual API call
        return {"status": "success"}

    def validate_passport_json(
        self,
        local_json: Union[str, dict],
        use_local_schema: bool = False,
    ) -> bool:
        """
        Validate a local OceanOPS passport JSON against a schema.

        Args:
            local_json (Union[str, dict]): Path to JSON file or dict object
                to validate.
            use_local_schema (bool, optional): If True, use the local
                schema file. Defaults to False (uses online schema).

        Returns:
            bool: True if JSON is valid against the schema.

        Raises:
            FileNotFoundError: If local schema file does not exist.
            ValueError: If local_json is not a file path or dictionary.
            requests.HTTPError: If online schema cannot be fetched.
            jsonschema.ValidationError: If JSON does not conform to schema.
        """
        if use_local_schema:
            schema_path = self.LOCAL_SCHEMA_PATH

            if not schema_path.exists():
                raise FileNotFoundError(f"Local schema not found: {schema_path}")

            print(f"Using LOCAL schema: {schema_path}")
            with open(schema_path, "r", encoding="utf-8") as f:
                schema = json.load(f)
        else:
            print("Using ONLINE OceanOPS schema")
            resp = requests.get(self.DEFAULT_SCHEMA_URL)
            resp.raise_for_status()
            schema = resp.json()

        if isinstance(local_json, (str, Path)):
            with open(local_json, "r", encoding="utf-8") as f:
                data = json.load(f)
        elif isinstance(local_json, dict):
            data = local_json
        else:
            raise ValueError("local_json must be a file path or a dictionary")

        validate(instance=data, schema=schema)

        print("JSON is valid against the schema")
        return True
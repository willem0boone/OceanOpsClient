import json
import requests
from typing import Any, Dict, Union, Optional
from pathlib import Path
from jsonschema import validate
from OceanOpsClient.config import Settings


class OceanOpsClient:
    """
    Client for interacting with the OceanOPS API.

    Provides methods for read-only data retrieval and authenticated
    data submission. Supports JSON schema validation of OceanOPS
    "passport" files.

    :cvar BASE_URL: Base URL for OceanOPS API endpoints.
    :type BASE_URL: str :noindex:
    :cvar DEFAULT_SCHEMA_URL: URL to the default passport JSON schema.
    :type DEFAULT_SCHEMA_URL: str :noindex:
    :ivar settings: Optional credentials/settings.
    :vartype settings: Optional[Settings]
    """

    BASE_URL = "https://www.ocean-ops.org/api/data"
    DEFAULT_SCHEMA_URL = (
        "https://www.ocean-ops.org/passports/examples/a-passport-input.schema.json"
    )

    def __init__(self, settings: Optional["Settings"] = None) -> None:
        """
        Initialize an OceanOps client.

        :param settings: Optional credentials/settings. If None, client operates in read-only mode.
        :type settings: Optional[Settings]
        """
        self.settings = settings

    @classmethod
    def from_env(cls, env_file: Optional[str] = None) -> "OceanOps":
        """
        Create an OceanOps client from environment variables or a .env file.

        :param env_file: Path to a .env file. If None, uses default environment variables.
        :type env_file: Optional[str]
        :return: Instance of OceanOps client. If credentials cannot be loaded, returns a read-only client.
        :rtype: OceanOps
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

        :param key_id: API key ID.
        :type key_id: str
        :param token: API key token.
        :type token: str
        :return: Instance of OceanOps client with credentials.
        :rtype: OceanOps
        """
        settings = Settings(API_KEY_ID=key_id, API_KEY_TOKEN=token)
        return cls(settings)

    def get_platform(self, ptfWigosId: str) -> Dict[str, Any]:
        """
        Retrieve platform information from OceanOPS using a WIGOS ID.

        :param ptfWigosId: Platform WIGOS ID.
        :type ptfWigosId: str
        :return: JSON response from the OceanOPS API.
        :rtype: Dict[str, Any]
        :raises ValueError: If ptfWigosId is not provided.
        :raises requests.HTTPError: If the API request fails.
        """
        if not ptfWigosId:
            raise ValueError("ptfWigosId must be provided")

        url = f"{self.BASE_URL}/platform/wigosid/{ptfWigosId}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def validate_passport_json(
            self,
            local_json: Union[str, dict],
            schema_source: Union[str, Path, None] = None,
    ) -> bool:
        """
        Validate a local OceanOPS passport JSON against a schema.

        :param local_json: Path to JSON file or dict object to validate.
        :param schema_source: If provided, use this local schema file path or a URL.
                              Defaults to online schema.
        :return: True if JSON is valid against the schema.
        """
        # --- Load schema ---
        if schema_source is None:
            # Default: online schema
            print("Using ONLINE OceanOPS schema")
            resp = requests.get(self.DEFAULT_SCHEMA_URL)
            resp.raise_for_status()
            schema = resp.json()
        else:
            # User-provided local schema
            schema_path = Path(schema_source)
            if not schema_path.exists():
                raise FileNotFoundError(
                    f"Schema file not found: {schema_path}")
            print(f"Using USER-PROVIDED local schema: {schema_path}")
            with open(schema_path, "r", encoding="utf-8") as f:
                schema = json.load(f)

        # --- Load JSON to validate ---
        if isinstance(local_json, (str, Path)):
            with open(local_json, "r", encoding="utf-8") as f:
                data = json.load(f)
        elif isinstance(local_json, dict):
            data = local_json
        else:
            raise ValueError("local_json must be a file path or a dictionary")

        # --- Validate ---
        validate(instance=data, schema=schema)
        print("JSON is valid against the schema")
        return True

    def post_passport(
            self,
            payload: Union[str, Path, Dict[str, Any]],
            dry_run: bool = True
    ) -> Dict[str, Any]:
        """
        Push a passport JSON payload to OceanOPS.

        Headers are generated only for this request using the secret token.

        :param payload: Either:
            - A path to a local JSON file containing the passport payload, or
            - A Python dictionary representing the payload.
        :type payload: Union[str, Path, Dict[str, Any]]
        :param dry_run: If True, sets options.dryRun to True to prevent real updates.
        :type dry_run: bool
        :return: Response from the API as a Python dictionary.
        :rtype: Dict[str, Any]
        :raises RuntimeError: If credentials are missing or request fails.
        """
        if not self.settings:
            raise RuntimeError("Cannot push data: credentials required")

        # Build ephemeral headers
        headers = {
            "Content-Type": "application/json",
            "X-OceanOPS-Metadata-ID": self.settings.API_KEY_ID,
            "X-OceanOPS-Metadata-Token": self.settings.API_KEY_TOKEN.get_secret_value(),
        }

        # Load payload if it's a file path
        if isinstance(payload, (str, Path)):
            payload_path = Path(payload)
            if not payload_path.exists():
                raise FileNotFoundError(
                    f"Payload JSON file not found: {payload}")
            with open(payload_path, "r", encoding="utf-8") as f:
                payload = json.load(f)
        elif not isinstance(payload, dict):
            raise ValueError(
                "Payload must be a JSON file path or a dictionary")

        # Ensure dryRun option is set
        payload.setdefault("options", {})["dryRun"] = dry_run

        url = f"{self.BASE_URL}/passports/submissions"

        # print(url)
        # print(headers)
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Passport submission failed: {e}") from e

        try:
            return response.json()
        except json.JSONDecodeError:
            return {"raw_text": response.text}

    def post_get_id(
            self,
            program: str,
            start_date: str,
            model: str,
            batch_status: str,
            longitude: float,
            latitude: float,
    ) -> Dict[str, Any]:
        """
        Request a single platform identifier from OceanOPS.

        :param program: Program name (e.g., "Argo CANADA")
        :param start_date: Deployment/start date (ISO format)
        :param model: Platform model (e.g., "APEX")
        :param batch_status: Batch status (e.g., "IN STOCK")
        :param longitude: Deployment longitude
        :param latitude: Deployment latitude
        :return: Result for the requested identifier
        :rtype: Dict[str, Any]
        :raises RuntimeError: If credentials are missing or request fails
        """

        if not self.settings:
            raise RuntimeError("Cannot request ID: credentials required")

        headers = {
            "Content-Type": "application/json",
            "X-OceanOPS-Metadata-ID": self.settings.API_KEY_ID,
            "X-OceanOPS-Metadata-Token": self.settings.API_KEY_TOKEN.get_secret_value(),
        }

        # API expects a list → wrap single request
        payload = [{
            "program": program,
            "startDate": start_date,
            "model": model,
            "batchStatus": batch_status,
            "longitude": longitude,
            "latitude": latitude,
        }]

        url = f"{self.BASE_URL}/platforms/getid"

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Get ID request failed: {e}") from e

        try:
            result = response.json()
        except json.JSONDecodeError:
            return {"raw_text": response.text}

        # API returns a list → extract first element for convenience
        if isinstance(result, list) and result:
            return result[0]

        raise RuntimeError("Unexpected response format from OceanOPS API")



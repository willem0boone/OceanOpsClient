Usage
==================

Credentials safety
------------------
Avoid exposing credentials in your code. Store them in a :code:`.env` file in the project root:

.. code-block:: dotenv

    API_KEY_ID=1234
    API_KEY_TOKEN=abcdefghijklmnopqrstuvwxyz

The client reads these values with :code:`pydantic-settings` when you call :code:`OceanOpsClient.from_env()`.

.. code-block:: python

    from OceanOpsClient import OceanOpsClient

    client = OceanOpsClient.from_env()
    print(client.settings)

If the environment variables are not present, :code:`from_env()` falls back to a read-only client and :code:`client.settings` will be :code:`None`.

This is the same pattern used by the repository example script:

.. code-block:: python

    from OceanOpsClient import OceanOpsClient

    client = OceanOpsClient.from_env()
    print(client.settings)

When credentials are configured, the output looks like this:

.. code-block::

    API_KEY_ID='1234' API_KEY_TOKEN=SecretStr('**********')

Under no circumstances will the client display your secret token in plain text.

Create a client explicitly
--------------------------
If you prefer to pass credentials directly, use :code:`from_credentials()`:

.. code-block:: python

    from OceanOpsClient import OceanOpsClient

    client = OceanOpsClient.from_credentials("1234", "abcdefghijklmnopqrstuvwxyz")
    print(client.settings)

Read-only lookups
-----------------
The library can be used without credentials for read-only lookups.

Pull a platform by WIGOS ID:

.. code-block:: python

    from pprint import pprint
    from OceanOpsClient import OceanOpsClient

    client = OceanOpsClient()
    wigos_id = "0-22000-0-6204817"
    response = client.get_by_wigosID(ptfWigosId=wigos_id)
    pprint(response)

Lookup by internal ID:

.. code-block:: python

    from OceanOpsClient import OceanOpsClient

    client = OceanOpsClient()
    response = client.get_by_internalID("007", program="1006434")
    print(response)

Lookup by PLF ID:

.. code-block:: python

    from OceanOpsClient import OceanOpsClient

    client = OceanOpsClient()
    response = client.get_by_plfID(1305758, program="1006434")
    print(response)

Validate a passport
-------------------
Passport validation works without credentials and returns a tuple:
:code:`(True, None)` for valid data, or :code:`(False, "<error message>")` for invalid data.

.. code-block:: python

    from OceanOpsClient import OceanOpsClient

    client = OceanOpsClient()
    passport = "passport_thornton_buoy.json"
    status = client.validate_passport_json(passport)
    print(status)

Push a passport
---------------
For authenticated writes, make sure your :code:`.env` file is available and use :code:`from_env()`.

.. code-block:: python

    from pprint import pprint
    from OceanOpsClient import OceanOpsClient

    client = OceanOpsClient.from_env()

    passport = "passport_thornton_buoy.json"
    validation = client.validate_passport_json(passport)
    print(validation)

    result = client.post_passport(passport, dry_run=True)
    pprint(result)

The :code:`dry_run=True` option is the safest way to test a push request without making a real update.

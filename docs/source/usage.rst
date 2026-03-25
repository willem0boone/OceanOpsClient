Usage
==================
Credentials safety
------------------
Avoid exposing credentials in your code!
Instead use a :code:`.env` file:

.. code-block:: python

    API_KEY_ID = "****"
    API_KEY_TOKEN = "************************"


And initiate using:

.. code-block:: python

    from OceanOpsClient.OceanOpsClient import OceanOps

    client = OceanOps.from_env()
    print(client.settings)




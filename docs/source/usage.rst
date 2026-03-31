Usage
==================
Credentials safety
------------------
Avoid exposing credentials in your code.
Instead use a :code:`.env` file with key and token:

.. code-block:: python

    API_KEY_ID = "1234"
    API_KEY_TOKEN = "abcdefghijklmnopqrstuvwxyz"


Initiate using:

.. code-block:: python

    from OceanOpsClient import OceanOpsClient
    client = OceanOpsClient.from_env()

The credentials are in pydantic safe settings

.. code-block:: python

        print(client.settings)

This will return:

.. code-block::

    API_KEY_ID='1234' API_KEY_TOKEN=SecretStr('**********')

Under no circumstances the client will display your secret token.


Pull a platform
---------------

.. code-block:: python

    from pprint import pprint
    from OceanOpsClient import OceanOpsClient

    wigosID = "0-22000-0-6204817"
    client = OceanOpsClient()
    resp = client.get_platform(ptfWigosId=wigosID)
    pprint(resp)

This will return:

.. code-block::

    {'data': [{'activityCriterion': 0,
               'batchRequestRef': '2026-02-09T10:15:54Z-Other Met Moored Buoy',
               'closureCriterion': 0,
               'creatorId': None,
               'dataUrl': None,
               'deleteTag': None,
               'description': 'Moored surface buoy that serves both ERICs ICOS and '
                              'LifeWatch. The buoy is equipped with sensors for '
                              'pCO2, dissolved oxygen, temperature, salinity, '
                              'fluorescence (chl-a), turbidity, passive acoustic '
                              'receiver. Sensors are deployed approx 1m below sea '
                              'surface. Station is visited on a monthly basis in '
                              'order to collect samples for validation/calibration '
                              'of sensors and maintain/replace equipment. Station '
                              'has a secure and stable communication with VLIZ '
                              'servers for NRT data transmission and overall '
                              'interactive communication with in situ equipment',
               'eNotificationDate': None,
               'endingDate': None,
               'id': 1305758,
               'ingestionMethodId': None,
               'insertDate': '2026-02-09T10:15:54.647171',
               'lastLocId': None,
               'lastUpdate': None,
               'metadataAvailable': None,
               'name': 'ICOS STATION Thornton Buoy',
               'nokReason': None,
               'passportValid': None,
               'platform_asset_id': None,
               'ref': '6204817',
               'refParent': None,
               'sourceText': None,
               'updateDate': '2026-02-16T08:06:10.511361',
               'validated': None,
               'wigosSynchronised': None}],
     'total': 1}

Validate Passport
-----------------

.. code-block:: python

    from OceanOpsClient import OceanOpsClient
    client = OceanOpsClient()
    passport = "passport_thornton_buoy.json"
    status = client.validate_passport_json(passport)
    print(status)


The status is a tuple: Tuple (True, None) if valid, otherwise (False, error message)

Push passport
-------------
For pushing a passport you need credentials.
Make sure to have a valid .env file in the repository.

.. code-block:: python

    from pprint import pprint
    from OceanOpsClient import OceanOpsClient

    client = OceanOpsClient.from_env()

    passport = "passport_thornton_buoy.json"
    status = client.validate_passport_json(passport)
    print(status)

    m = client.post_passport(passport, dry_run=True)
    pprint(m)

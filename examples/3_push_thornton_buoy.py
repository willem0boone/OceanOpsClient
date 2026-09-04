from pprint import pprint
from OceanOpsClient import OceanOpsClient

client = OceanOpsClient.from_env()

passport = "passport_thornton_buoy.json"
# client.validate_passport_json(passport)

m = client.post_passport(passport, dry_run=True)
pprint(m)

from pprint import pprint
from OceanOpsClient.OceanOpsClient import OceanOps

client = OceanOps.from_env()

passport = "passport_thornton_buoy.json"
# client.validate_passport_json(passport)

print(client.settings)

m = client.post_passport(passport, dry_run=False)
pprint(m)

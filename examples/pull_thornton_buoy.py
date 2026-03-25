from pprint import pprint
from OceanOpsClient.OceanOpsClient import OceanOps

wigosID = "0-22000-0-6204817"
client = OceanOps()
resp = client.get_platform(ptfWigosId=wigosID)
pprint(resp)

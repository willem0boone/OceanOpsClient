from pprint import pprint
from OceanOpsClient import OceanOpsClient

client = OceanOpsClient()

print("-"*50)
wigosID = "0-22000-0-6204817"
resp = client.get_by_wigosID(ptfWigosId=wigosID)
pprint(resp)

print("-"*50)
plf_id = 1305758
resp = client.get_by_plfID(plf_id=plf_id)
pprint(resp)

print("-"*50)
internal_id = "007"
resp = client.get_by_internalID(internal_id=internal_id)
pprint(resp)


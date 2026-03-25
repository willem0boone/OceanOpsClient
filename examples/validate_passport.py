from OceanOpsClient.OceanOpsClient import OceanOps

client = OceanOps()
passport = "passport_thornton_buoy.json"
client.validate_passport_json(passport, use_local_schema=True)

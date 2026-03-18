from OceanOpsClient.OceanOpsClient import OceanOps

client = OceanOps.from_env()
print(client.settings)



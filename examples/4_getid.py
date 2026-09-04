from OceanOpsClient import OceanOpsClient

client = OceanOpsClient.from_env()

# only works if you have a .env file in this directory with
# API_KEY_ID = ""
# API_KEY_TOKEN = ""

program = "vliz-arms-mbon"
start_date = "2026-06-15T12:00:00"
longitude = 4.6
latitude = 51.2

print(client.settings)

test = client.post_get_id(program=program, start_date=start_date, longitude=longitude, latitude=latitude)
print(test)



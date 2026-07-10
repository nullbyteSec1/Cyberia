import json
with open("config.json","r",encoding="utf-8") as config:
    data = json.load(config)


hosting = data["hosting"]
porting = data["porting"]
secret_key = data["secret_key"]
upload_folder = data["upload_folder"]

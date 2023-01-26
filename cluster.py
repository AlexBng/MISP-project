import json
import os

def ajout_incident(cluster, incident):
        meta = {}
        for key, value in incident.items():
                meta[key] = value

        new_value = {
                "meta": meta,
                "uuid": os.popen("uuidgen").read().strip().lower(),
                "value": incident["Description"],
        }

        cluster["values"].append(new_value)

with open('cluster.json', 'r') as f:
    cluster = json.load(f)

with open('data.txt', 'r') as f:
    for line in f:
        data = json.loads(line)
        ajout_incident(cluster,data)


with open('cluster.json', 'w') as f:
    cluster = json.dump(cluster, f,indent=4)


import json
from collections import OrderedDict

all_data = OrderedDict({"randread.json": "read",
                        "randwrite.json": "write",
                        "read.json": "read",
                        "write.json": "write"})

csv = ""
keys = all_data.keys()
keys = [x.split(".")[0] for x in keys]
csv += ",".join(keys)
csv += "\n"

iops_list = []
for k, v in all_data.items():
    with open(k) as f:
        data = json.load(f)
        iops = int(data["jobs"][0][v]["iops"])
        iops_list.append(str(iops))

csv += ",".join(iops_list)
with open("data.csv", "w") as f:
    f.write(csv)

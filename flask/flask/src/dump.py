import urllib.request
import json
from collections import deque

URL="http://localhost:5001/api/node/%s"

def get_json(nid):
    print(URL % nid)
    data = urllib.request.urlopen(URL % nid).read().decode("utf-8")
    with open("%s.json" % nid, "w") as f:
        f.write(data)
    data = json.loads(data)
    return sorted([c["id"] for c in data["result"]["children"]])

def get_json_graph(nid):
    togo = deque([nid])
    seen = set()
    while togo:
        nid = togo.popleft()
        if nid in seen:
            continue
        seen.add(nid)
        togo.extend(get_json(nid))
    return seen

if __name__ == "__main__":
    get_json_graph(7)

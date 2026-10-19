import csv, io, json, urllib.request
from datetime import datetime, timezone

URL = "https://raw.githubusercontent.com/chadwickbureau/register"

upstream_commit = json.load(urllib.request.urlopen("https://api.github.com/repos/chadwickbureau/register/commits/master"))["sha"]

pairs = []
for d in "0123456789abcdef":
    url = f"{URL}/master/data/people-{d}.csv"
    text = urllib.request.urlopen(url).read().decode("utf-8")
    for row in csv.DictReader(io.StringIO(text)):
        if row["key_fangraphs"] and row["key_bbref"]:
            pairs.append([row["key_fangraphs"], row["key_bbref"]])


data = {
    "schemaVersion": 1,
    "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    "upstreamCommit": upstream_commit,
    "source": "Chadwick Baseball Bureau Register",
    "sourceUrl": "https://github.com/chadwickbureau/register",
    "license": "ODC-By 1.0",
    "licenseUrl": "http://opendatacommons.org/licenses/by/1.0/",
    "attribution": "Player ID data from the Chadwick Baseball Bureau Register, licensed under ODC-By 1.0.",
    "modified": "Filtered to FanGraphs and Baseball-Reference ID pairs.",
    "pairs": pairs
}

with open("data.json", "w") as file:
    json.dump(data, file, indent=4)

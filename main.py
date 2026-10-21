import csv, io, json, urllib.request
from datetime import datetime, timezone

URL = "https://raw.githubusercontent.com/chadwickbureau/register"

upstream_commit = json.load(urllib.request.urlopen("https://api.github.com/repos/chadwickbureau/register/commits/master"))["sha"]

players = []
for d in "0123456789abcdef":
    url = f"{URL}/master/data/people-{d}.csv"
    text = urllib.request.urlopen(url).read().decode("utf-8")
    for row in csv.DictReader(io.StringIO(text)):
        mlb = row["key_mlbam"] or ""
        fg = row["key_fangraphs"] or ""
        bref = row["key_bbref"] or ""
        if mlb or fg or bref:
            players.append([mlb, fg, bref])


data = {
    "schemaVersion": 2,
    "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    "upstreamCommit": upstream_commit,
    "source": "Chadwick Baseball Bureau Register",
    "sourceUrl": "https://github.com/chadwickbureau/register",
    "license": "ODC-By 1.0",
    "licenseUrl": "http://opendatacommons.org/licenses/by/1.0/",
    "attribution": "Player ID data from the Chadwick Baseball Bureau Register, licensed under ODC-By 1.0.",
    "modified": "Filtered to only MLBAM, Baseball-Reference, and FanGraphs IDs.",
    "players": players
}

with open("data.json", "w") as file:
    json.dump(data, file, indent=4)

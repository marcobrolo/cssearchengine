import json
import sqlite3
from pprint import pprint


uniq = set()
fp = open("rmp.json")
profs = json.load(fp)

for p in profs:
    uniq.add((p['last_name'], p['first_name'], p['clarity'], p['helpfulness'], p['easiness'],))

print uniq
profs = list(uniq)
profs.sort(key=lambda x: x[0])
# pprint(profs)

conn = sqlite3.connect("eg.db")
c = conn.cursor()
c.executemany("INSERT INTO engine_prof (last_name, first_name, clarity, helpfulness, easiness) VALUES(?, ?, ?, ?, ?)", profs)
conn.commit()
conn.close()

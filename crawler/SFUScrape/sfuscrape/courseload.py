import json
import sqlite3
from pprint import pprint


uniq = set()
fp = open("courses.json")
courses = json.load(fp)

for c in courses:
    uniq.add((c['course_name'], c['course_desc'],))

courses = list(uniq)
courses.sort(key=lambda x: x[0])
# pprint(profs)

conn = sqlite3.connect("eg.db")
c = conn.cursor()
c.executemany("INSERT INTO engine_course (code, name) VALUES(?,?)", courses)
conn.commit()
conn.close()
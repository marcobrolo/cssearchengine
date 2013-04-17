import json
import sqlite3
from pprint import pprint

file_counter = 1
while(1):
	file_name = "profdata"+ str(file_counter)
	file_path = file_name
	file_counter += 1
	try:
		fp = open(file_path)
		profs = json.load(fp)
		for p in profs:
			print "WWWWWWW", p
	except:
		print("failed to open ", file_path)
		exit()


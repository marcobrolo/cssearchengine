import json
import sqlite3 as lite
from pprint import pprint
import re

file_counter = 1

computing_naming_list = ['cmpt', 'comp', 'computing', 'macm', 'campt']
invalid_course_names = []
while(1):
	file_name = "profdata"+ str(file_counter)
	file_path = "prof_files/" + file_name
	file_counter += 1
	try:
		fp = open(file_path)
		profs = json.load(fp)
	except:
		print(invalid_course_names)
		exit()
	
#	fp = open(file_path)
#	profs = json.load(fp)
	prof_name_last = profs["last_name"]
	course_list = profs["course_rating"]
	course_name =''
	course_number = ''
	course_clarity = ''
	course_easiness =''
	course_helpfulness =''
	print course_list, "\n"

	for courseID, rank in course_list.iteritems():
		course_clarity = ''
		course_easiness =''
		course_helpfulness =''
		courseID = courseID.lower()
		courseID = courseID.replace(" ",'')
		courseID = courseID.replace("\n",'')

		word_split = re.split('(\d+)', courseID)
		try:
			course_name = word_split[0]
			course_number = word_split[1]
		except:
			print "ERROR:::::::::::::::::: ", courseID, file_name
			invalid_course_names.append((courseID, file_name))
			continue

		if course_name not in computing_naming_list:
			#print courseID, " is not a valid course"
			continue
		else:
			for rank_name, rank_score in rank.iteritems():
				if rank_name == "clarity":
					course_clarity = rank_score
				elif rank_name == "helpfulness":
					course_helpfulness = rank_score
				elif rank_name == "easiness":
					course_easiness = rank_score


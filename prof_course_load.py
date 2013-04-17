import json
import sqlite3 as lite
from pprint import pprint
import re

file_counter = 1

computing_naming_list = ['cmpt', 'comp', 'computing', 'macm', 'campt']
invalid_course_names = []
con = lite.connect('eg.db')
prof_list_db_dict = {}
prof_list_db_lastname = []
course_list_db = []
course_list_db_dict = {}

# get prof last name and id in table
# get courseid and id in table
# store them in list so we can retrieve id for uses later
with con:    
    cur = con.cursor()    
    cur.execute("SELECT * FROM engine_prof")
    
    while(True):
    	# fetch prof items from db and add into offline lists for post processing
    	row = cur.fetchone()
    	if row == None:
        	break
        if row[1] not in prof_list_db_lastname:
        	prof_list_db_lastname.append(row[1].strip().lower())
        	prof_list_db_dict[row[1]] = row[0]

    cur = con.cursor()
    cur.execute("SELECT * FROM engine_course")
    while(True):
    	row = cur.fetchone()
    	if row == None:
    		break
    	if row[1] not in  course_list_db:
    		course_list_db.append(row[1])
    		course_list_db_dict[row[1]] = row[0]

f = open('prof_last_name_db.txt', 'w')
for items in prof_list_db_lastname:
	f.write(items)
	f.write('\n')
f.close()

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
	prof_name_last = profs["last_name"].strip()
	prof_name_check = profs["last_name"].strip().lower()
	course_list = profs["course_rating"]
	course_name =''
	course_number = ''
	course_clarity = '0'
	course_easiness ='0'
	course_helpfulness ='0'
	print course_list, "\n"

	for courseID, rank in course_list.iteritems():
		course_clarity = '0'
		course_easiness ='0'
		course_helpfulness ='0'
		course_comment = ''
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
			f = open('error_prof_name.txt', 'w')
			for rank_name, rank_score in rank.iteritems():
				if rank_name == "clarity":
					course_clarity = rank_score
				elif rank_name == "helpfulness":
					course_helpfulness = rank_score
				elif rank_name == "easiness":
					course_easiness = rank_score
				elif rank_name == "comment":
					course_comment = rank_score
			courseID_db = "CMPT" + str(course_number)
			if courseID_db in course_list_db:
				if prof_name_check in prof_list_db_lastname:
					cur.execute("insert into engine_courserating (course_id, prof_id, easiness, helpfulness, clarity, comments) values (?, ?, ?, ?, ?, ?)",
		            (course_list_db_dict[courseID_db], prof_list_db_dict[prof_name_last], course_easiness, course_helpfulness, course_clarity, course_comment))
		    		con.commit()
		    	elif prof_name_check not in prof_list_db_lastname:
		    		print "ERROR", prof_name_check, "not in db"
		    		f.write(prof_name_check)
		    		f.write('\n')
		    	f.close()
		    #else:
		    #	print "ERROR:", courseID_db, " no in db"
#trim ro strip nanmes

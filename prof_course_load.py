import json
import sqlite3 as lite
from pprint import pprint
import re
import Levenshtein as lev

file_counter = 1

computing_naming_list = ['cmpt', 'comp', 'computing', 'macm', 'campt']
invalid_course_names = []
con = lite.connect('eg.db')
prof_list_db_fullname = []
prof_list_db_lastname = []
prof_list_repeated_lastnames = []
prof_list_db_dict = {}
prof_not_in_db_list= []
prof_firstname_id_dict ={}
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
    	prof_firstname_id_dict = {}
    	row = cur.fetchone()
    	if row == None:
        	break
        if row[1] not in prof_list_db_lastname:
        	prof_list_db_lastname.append(row[1])
        	prof_firstname_id_dict[row[2]] = row[0]
        	prof_list_db_dict[row[1]] = prof_firstname_id_dict
        	prof_list_db_fullname.append((row[2]+row[1]))
        else:
        	prof_firstname_id_dict[row[2]] = row[0]
        	for key, value in prof_list_db_dict[row[1]].iteritems():
        		prof_firstname_id_dict[key] = value
        	prof_list_db_dict[row[1]] = (prof_firstname_id_dict)
        	for key, value in prof_list_db_dict[row[1]].iteritems():
        		print "EEEEEEEEEEE multiple lsat names", row[1], key 
        		prof_firstname_id_dict[key] = value
        	prof_list_db_fullname.append((row[2]+row[1]))
        	prof_list_repeated_lastnames.append((row[1],row[2]))
        	print "we got same last names ", row[1]

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
	prof_name_last = profs["last_name"]
	prof_name_check = profs["last_name"]
	prof_name_first = profs["first_name"]
	prof_name_full = profs["first_name"]+profs["last_name"]
	course_list = profs["course_rating"]
	course_name =''
	course_number = '0'
	course_clarity = '0'
	course_easiness ='0'
	course_helpfulness ='0'
	#print course_list, "\n"

	#figure out alternative names and same last names
	if prof_name_last in prof_list_db_lastname:
		# we got same last name but figure out first name
		lev_ratio = 0.0
		for possible_prof in prof_list_db_dict[prof_name_last]:
			#print "WTF", possible_prof
			#find same last name dif first name
			if lev.ratio(possible_prof, prof_name_first) > lev_ratio:
				#print"fixing name", prof_name_full, prof_name_first, possible_prof
				prof_name_first = possible_prof
				prof_name_full = prof_name_first+profs["last_name"]
				#print "now", prof_name_full

	for courseID, rank in course_list.iteritems():
		course_clarity = '0'
		course_easiness ='0'
		course_helpfulness ='0'
		course_comment = 'N/A'
		courseID = courseID.lower()
		courseID = courseID.replace(" ",'')
		courseID = courseID.replace("\n",'')

		word_split = re.split('(\d+)', courseID)
		try:
			course_name = word_split[0]
			course_number = word_split[1]
		except:
			#print "ERROR:::::::::::::::::: ", courseID, file_name
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
				elif rank_name == "comment":
					course_comment = rank_score
			courseID_db = "CMPT" + str(course_number)
			if (courseID_db in course_list_db) and (prof_name_last in prof_list_db_lastname):
				# get proper prof db id
				db_id = ''
				for key, value in prof_list_db_dict[prof_name_last].iteritems():
					if key == prof_name_first:
						db_id = value
				if db_id == '':
					print "EEEEEEEEEEEEE db_id not avail maybe matching prof dictionary no good", prof_name_first, prof_name_last, db_id
				if prof_name_check in prof_list_db_lastname:
					cur.execute("insert into engine_courserating (course_id, prof_id, easiness, helpfulness, clarity, comments) values (?, ?, ?, ?, ?, ?)",
		            (course_list_db_dict[courseID_db], str(db_id), course_easiness, course_helpfulness, course_clarity, course_comment))
		    		con.commit()
		    		#print("finish commiting to db")
		    	elif prof_name_check not in prof_list_db_lastname:
		    		print "ERROR", prof_name_full, "not in db"
		    #else:
		    #	print "ERROR:", courseID_db, " no in db"
#trim ro strip nanmes

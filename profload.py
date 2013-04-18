import json
import sqlite3 as lite
from pprint import pprint
import Levenshtein as lev

file_counter = 1
con = lite.connect('eg.db')
prof_list_db_fullname = []
prof_list_db_lastname = []
prof_list_repeated_lastnames = []
prof_list_db_dict = {}
prof_not_in_db_list= []
prof_firstname_id_dict ={}

def get_prof_from_db(id):
	# printing out prof item in db based on the db id
    cur.execute("SELECT * FROM engine_prof WHERE Id="+str(id))
    row = cur.fetchone()
    if row == None:
                print "ERROR: our prof_list_db_dict id is not in DB"
                exit()
    return row

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
        	prof_list_db_fullname.append((row[2]+row[1]))
        	prof_firstname_id_dict[row[2]] = row[0]
        	prof_list_db_dict[row[1]] = prof_firstname_id_dict
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
print prof_list_db_fullname
while(1):
	print "file counter", file_counter
	file_name = "profdata"+ str(file_counter)
	file_path = "prof_files/" + file_name
	file_counter += 1
#	try:
#		fp = open(file_path)
#		profs = json.load(fp)
#	except:
#		print("list of profs not in db", prof_not_in_db_list)
#		exit()
	
	fp = open(file_path)
	profs = json.load(fp)
	prof_name_last = profs["last_name"]
	prof_name_first = profs["first_name"]
	prof_name_full = profs["first_name"]+profs["last_name"]

	#figure out alternative names and same last names
	if prof_name_last in prof_list_db_lastname:
		# we got same last name but figure out first name
		lev_ratio = 0.0
		for possible_prof in prof_list_db_dict[prof_name_last]:
			#print "WTF", possible_prof
			#find same last name dif first name
			if lev.ratio(possible_prof, prof_name_first) > lev_ratio:
				print"fixing name", prof_name_full, prof_name_first, possible_prof
				prof_name_first = possible_prof
				prof_name_full = prof_name_first+profs["last_name"]
				print "now", prof_name_full

	if prof_name_last not in prof_list_db_lastname:
		print prof_name_last, " not in db"
		prof_not_in_db_list.append(prof_name_full)
		continue
	else:
		if prof_name_full not in prof_list_db_fullname:
			prof_not_in_db_list.append(prof_name_full)
			print "EEEEEEEEEE", prof_name_full, "different first names"
			continue
		elif prof_name_full in prof_list_db_fullname:
			#print prof_name_full , " prof id is", prof_list_db_dict[prof_name_last]
			db_id = ''
			for key, value in prof_list_db_dict[prof_name_last].iteritems():
				if key == prof_name_first:
					db_id = value
			if db_id == '':
				print "EEEEEEEEEEEEE db_id not avail maybe matching prof dictionary no good"

			cur.execute("SELECT * FROM engine_prof WHERE Id="+str(db_id))
			row = cur.fetchone()
			if row == None:
				print "ERROR: our prof_list_db_dict id is not in DB"
				exit()
			# begin adding in the ratings
			print db_id, prof_name_full
			#print "before update ranks", get_prof_from_db(str(db_id))
			cur.execute("UPDATE engine_prof SET helpfulness=?, clarity=?, easiness=? WHERE Id=?", (profs["helpfulness"], profs["clarity"], profs["easiness"], str(db_id)))        
    		con.commit()
    		#print "after update ranks ", get_prof_from_db(db_id)
			# we can start adding in the values of scrapped data
		#print prof_name, " in db"
		continue



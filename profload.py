import json
import sqlite3 as lite
from pprint import pprint

file_counter = 1
con = lite.connect('eg.db')
prof_list_db_fullname = []
prof_list_db_lastname = []
prof_list_repeated_lastnames = []
prof_list_db_dict = {}
prof_not_in_db_list= []


def get_prof_from_db(id):
	# printing out prof item in db based on the db id
    cur.execute("SELECT * FROM engine_prof WHERE Id="+str(prof_list_db_dict[prof_name_last]))
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
    	row = cur.fetchone()
    	if row == None:
        	break
        if row[1] not in prof_list_db_lastname:
        	prof_list_db_lastname.append(row[1])
        	prof_list_db_fullname.append((row[2]+row[1]))
        	prof_list_db_dict[row[1]] = row[0]
        else:
        	prof_list_db_fullname.append((row[2]+row[1]))
        	prof_list_repeated_lastnames.append((row[1],row[2]))
        	print "we got same last names ", row[1]
print prof_list_db_fullname
while(1):
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
	prof_name_full = profs["first_name"]+profs["last_name"]
	if prof_name_last not in prof_list_db_lastname:
		print prof_name_last, " not in db"
		prof_not_in_db_list.append(prof_name_full)
		continue
	else:
		if prof_name_full not in prof_list_db_fullname:
			prof_not_in_db_list.append(prof_name_full)
			#print prof_name_full, "has shortened name"
			continue
		else:
			#print prof_name_full , " prof id is", prof_list_db_dict[prof_name_last]
			cur.execute("SELECT * FROM engine_prof WHERE Id="+str(prof_list_db_dict[prof_name_last]))
			row = cur.fetchone()
			if row == None:
				print "ERROR: our prof_list_db_dict id is not in DB"
				exit()
			# begin adding in the ratings
			print "before update ranks", get_prof_from_db(str(prof_list_db_dict[prof_name_last]))
			cur.execute("UPDATE engine_prof SET helpfulness=?, clarity=?, easiness=? WHERE Id=?", (profs["helpfulness"], profs["clarity"], profs["easiness"], str(prof_list_db_dict[prof_name_last])))        
    		con.commit()
    		print "after update ranks ", get_prof_from_db(str(prof_list_db_dict[prof_name_last]))
			# we can start adding in the values of scrapped data
		#print prof_name, " in db"
		continue



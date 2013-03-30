from bs4 import BeautifulSoup
from urllib2 import urlopen

# url of ratemyprof's SFU compsci: index of all compsci profs
#BASE_URL = "http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=Computer+Science&orderby=TLName&sid=1482"
BASE_URL = 


# parse ratemyprof and download professor's webpage
# figure out how they wrap professors profile page links
# figure out how they wrap "next page" links to access
   #next pages for professors

def get_file(URL):
    try:
        file = urlopen(URL)
        contents = file.read()
        file.close()
        return contents
    except IOERROR:
        print("COULD NOT OPEN FILE %s" % URL )

def main():
    contents = get_file(BASE_URL)


if __name__ "__main__":
    main()

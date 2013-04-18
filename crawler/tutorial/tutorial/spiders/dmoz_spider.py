from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from tutorial.items import DmozItem
from tutorial.items import RateMyProfItem, Prof
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http.request import Request
from scrapy import signals
import os
import re
import json
from scrapy.xlib.pydispatch import dispatcher

class SFU_faculty_spider(BaseSpider):
    name = "sfufaculty"
    allowed_domains = ["cs.sfu.ca"]
    start_urls =[
        "http://www.cs.sfu.ca/people/faculty.html"
    ]

    def parse(self, response):
        first_name = ''
        last_name = ''
        prof_list = {}

        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[@class="textimage section"]')
        for site in sites:
            name_scrap = site.select('div[@class="ruled"]/div[@class="text"]/h3/text()').extract()
            name_scrap = str(name_scrap)[3:-2]
            print name_scrap
            name_scrap = name_scrap.split(",")[0]
            name_scrap = name_scrap.split(" ")
            print name_scrap
            first_name = name_scrap[0]
            if first_name != '':
                try:
                    last_name = name_scrap[2]
                except:
                    print name_scrap
                    last_name = name_scrap[1]

            print first_name, last_name



class RMPSpider(BaseSpider):
    counter = 1
    course_dict = {}
    prof = Prof()   # holds prof information links to django model using DjangoItem
    prof_list_dict ={}
    name = "ratemyprof"
    allowed_domains = ["ratemyprofessors.com"]
    start_urls = [
        "http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=Computer+Science&orderby=TLName&sid=1482",
        "http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=Computer+Science&orderby=TLName&sid=1482&pageNo=2",
        "http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=Computer+Science&orderby=TLName&sid=1482&pageNo=3",
        "http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=Computer+Science&orderby=TLName&sid=1482&pageNo=4",
        "http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=Computer+Science&orderby=TLName&sid=1482&pageNo=5",
        "http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=Computer+Science&orderby=TLName&sid=1482&pageNo=6",
        "http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=Computer+Science&orderby=TLName&sid=4267",
        "http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=Computer+Science&orderby=TLName&sid=4267&pageNo=2"
    ]
    def index_prof_name_extract_refine(self, name):
        '''
        refines scrapy extract method for ratemyprof 
        from main page
        and returns first_name last_name
        '''
        name = name[3:-2]
        name = name.split(',')
        first_name = ''
        last_name = ''
        try:
            first_name = name[0]
            last_name = name[1]
        except IndexError:
            print ("error", name[0])
            return first_name, last_name
        return first_name, last_name

    def prof_profile_extract_name(self, name):
        '''
        refines scrapy extract method for ratemyprof 
        from professor profile page
        and returns first_name last_name
        '''
        name = name.split("- ")[0]
        firstname = ''
        lastname = ''
        if "\\xa0" in name:
            name = name[3:]
            if " " in name:
                name = name.replace(" ","")
            name = name.replace("\\xa0", "_")
        try:
            firstname = name.split("_")[0]
            lastname = name.split("_")[1]
        except IndexError:
            print("error", name[0])
            return firstname, lastname
        return firstname, lastname

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[@class="profName"]')
        items = []
        for site in sites:
            prof_link = site.select('a/@href').extract()
            print "we are visiting", site.select('a/text()').extract()
            
            next_page = "http://www.ratemyprofessors.com/" + str(prof_link)[3:-2]            
            if next_page:
                yield Request(next_page, self.parseProfProfile)
        filename = "files/" + response.url.split("/")[-1]
        
        
        #open(filename, 'wb').write(response.body)
     
    
    def parseProfProfile(self, response):
        prof_dict = {}
        current_course_dict= {}
        hxs = HtmlXPathSelector(response)
        
        prof_profile_page_number = "1"
        url = response.url
        path = "//home//draco//Dropbox//SFU//cmpt456//project//cssearchengine//crawler//tutorial//files//"
        first_name =''      # used for djangoitem
        lastname = ''       # used for djangoitem
        name = 'N/A'           # used for filename for saving prof profile page
        quality = 'N/A'        # used for prof rating scrape from rmp site
        helpfulness = 'N/A'    # used for prof rating scrape from rmp site
        easiness = 'N/A'       # used for prof rating scrape from rmp site
        clarity = 'N/A'        # used for prof rating scrape from rmp site
        
        profList = []       # holds list of prof objects
        class_list = []     # holds list of class objects to store comments and ratings

        if "pageNo" in url:
            prof_profile_page_number = url.split("=")[-1]

        # used to determine if there are multi pages
        flag = False

        # grab prof information and save the page
        # grab prof name below
        sites = hxs.select('/html/head/title')
        f = open("prof_name_errors.txt", 'w')
        for site in sites:

            name = str(site.select('text()').extract())
            #print ":::::::::::::::::::::::::::::", name, url
            firstname, lastname = self.prof_profile_extract_name(name)
            # error check
            if firstname == '' and lastname == '':
                print name, "HAS ERRORS"
                f.write(name)
                f.write("\n")
            name = firstname + "_" + lastname
            print "WWWWWWWWW", name, str(self.counter)
        if not os.path.exists(path + name + "//"):
            os.makedirs(path+name+"//")
        f.close()
        # save prof page here    
        #filename = path + name + "//" + name + "_" + prof_profile_page_number
        #open(filename, 'wb').write(response.body)

        # get the score card
        # we only need to parse this once
        if flag == False:
            # get overall quality
            quality = str(hxs.select('//li[@id="quality"]').extract())
            try:
                quality = quality.split("strong>")[1][:-2]
            except:
                quality = ''
                print "quality issues", quality
            #print "Quality: ", quality

            # get helpfulness
            helpfulness = str(hxs.select('//li[@id="helpfulness"]').extract())
            try:
                helpfulness = helpfulness.split("strong>")[1][:-2]
            except:
                helpfulness = ''
                print "helpfulness issue", helpfulness
            #print "helpfulness: ", helpfulness

            # get clarity
            clarity = str(hxs.select('//li[@id="clarity"]').extract())
            try:
                clarity = clarity.split("strong>")[1][:-2]
            except:
                clarity = ''
                print "clarity issue", clarity
            #print "Clarity: ", clarity

            # get easiness
            easiness = str(hxs.select('//li[@id="easiness"]').extract())
            try:
                easiness = easiness.split("strong>")[1][:-2]
            except:
                easiness = ''
                print "easiness issue", easiness
            #print "Easiness: ", easiness

        # we now try to get classes and comments
        # EVEN
        sites = hxs.select('//div[@class="entry even"]')
                
        for site in sites:
            course_name = ''
            course_easiness = '0'
            course_clarity = '0'
            course_helpful ='0'
            course_comment = ''
            rating_dict = {}
            course_name = str(site.select('div[@class="class"]/p/text()').extract())[3:-2]
            ratings = site.select('div[@class="rating"]')
            for rating in ratings:
                ranks = rating.select('p')
                for rank in ranks:
                    rank_name = str(rank.select('strong/text()').extract())
                    rank_score = str(rank.select('span/text()').extract())
                    if rank_name[3:-2] == "Easiness":
                        course_easiness = rank_score[3:-2]
                    elif rank_name[3:-2] == "Helpfulness":
                        course_helpful = rank_score[3:-2]
                    elif rank_name[3:-2] == "Clarity":
                        course_clarity = rank_score[3:-2]
            course_comment = str(site.select('div[@class="comment"]/p[@class="commentText"]/text()').extract())
            try:
                course_comment = course_comment[2:-2]
            except:
                course_comment = ''
            rating_dict['easiness'] = course_easiness
            rating_dict['clarity'] = course_clarity
            rating_dict['helpfulness'] = course_helpful
            rating_dict['comment'] = course_comment
            current_course_dict[course_name] = rating_dict

        #ODD
        sites = hxs.select('//div[@class="entry odd"]')
        for site in sites:
            course_name = ''
            course_easiness = '0'
            course_clarity = '0'
            course_helpful ='0'
            course_comment = ''
            rating_dict = {}
            course_name = str(site.select('div[@class="class"]/p/text()').extract())[3:-2]
            ratings = site.select('div[@class="rating"]')
            for rating in ratings:
                ranks = rating.select('p')
                for rank in ranks:
                    rank_name = str(rank.select('strong/text()').extract())
                    rank_score = str(rank.select('span/text()').extract())
                    if rank_name[3:-2] == "Easiness":
                        course_easiness = rank_score[3:-2]
                    elif rank_name[3:-2] == "Helpfulness":
                        course_helpful = rank_score[3:-2]
                    elif rank_name[3:-2] == "Clarity":
                        course_clarity = rank_score[3:-2]
            course_comment = str(site.select('div[@class="comment"]/p[@class="commentText"]/text()').extract())
            try:
                course_comment = course_comment[2:-2]
            except:
                course_comment = ''
            rating_dict['easiness'] = course_easiness
            rating_dict['clarity'] = course_clarity
            rating_dict['helpfulness'] = course_helpful
            rating_dict['comment'] = course_comment
            current_course_dict[course_name] = rating_dict

        # we got our data, now make a prof item
        prof_dict['first_name'] = firstname
        prof_dict['last_name'] = lastname
        #prof['quality'] = quality
        prof_dict['clarity'] = clarity
        prof_dict['helpfulness'] = helpfulness
        prof_dict['easiness'] = easiness
        prof_dict['course_rating'] = current_course_dict
        self.prof_list_dict[firstname+lastname]=prof_dict
        #json_file_name = firstname+ "_"+ lastname + prof_profile_page_number + '.json'
        json_file_name = "profdata"+str(self.counter)
        #json_file_name = str(firstname) + "_" + str(lastname) + str(self.counter)
        #print json_file_name
        self.counter +=1
        json_path = "prof_files/" + json_file_name
        #print json_path
        with open(json_path, 'w') as outfile:
                json.dump(prof_dict, outfile, indent=4)
        outfile.close()

        # try item base approach
        item_prof = Prof()
        item_prof['last_name']=lastname
        item_prof['first_name']=firstname
        item_prof['helpfulness']=helpfulness
        item_prof['clarity']=clarity
        item_prof['easiness']=easiness
        item_prof['course_rating']=current_course_dict

 #Figure out if prof has next page and parse into next pages

        sites = hxs.select('//a[@class="next"]')
        for site in sites:
            flag = True
            next_page_url = site.extract().encode('ascii', 'ignore')
            next_page_url = str(next_page_url).split(" ")[1][6:-1]
            next_page_url = next_page_url.replace("&amp;","&")
            next_page_url = "http://www.ratemyprofessors.com" + next_page_url                 
        if flag == True:
            #print(name + " has a next page")
            self.prof_list_dict[firstname+lastname]=prof_dict
            yield Request(next_page_url, self.parseProfProfile)
        else:
            #print(name + " does not have a next page")
            prof_dict['course_rating'] = current_course_dict
            #print "WWWWWWWWWWWWWWWW", firstname, current_course_dict
            self.prof_list_dict[firstname+lastname]=prof_dict
            #print self.prof_list_dict
           # self.prof_list_dict[self.prof_dict['first_name']] = self.prof_dict
           # print self.prof_list_dict



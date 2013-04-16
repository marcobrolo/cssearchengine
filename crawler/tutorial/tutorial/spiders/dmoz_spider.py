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

class RMPSpider(BaseSpider):
    course_dict = {}
    prof = Prof()   # holds prof information links to django model using DjangoItem
    prof_list_dict ={}
    name = "ratemyprof"
    allowed_domains = ["ratemyprofessors.com"]
    start_urls = [
        "http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=Computer+Science&orderby=TLName&sid=1482"
        #"http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=Computer+Science&orderby=TLName&sid=1482&pageNo=2",
        #"http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=Computer+Science&orderby=TLName&sid=1482&pageNo=3",
        #"http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=Computer+Science&orderby=TLName&sid=1482&pageNo=4",
        #"http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=Computer+Science&orderby=TLName&sid=1482&pageNo=5",
        #"http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=Computer+Science&orderby=TLName&sid=1482&pageNo=6"
    ]
    rules = [
        Rule(SgmlLinkExtractor()),
        #Rule(SgmlLinkExtractor(allow=[r'SelectTeacher\.jsp\?the_dept=Computer\+Science&orderby=TLName&sid=1482&pageNo=\d+']), follow= True), 
        #Rule(SgmlLinkExtractor(allow=[r'\ShowRatings\\.jsp\\?tid=\d+']), callback = 'parseProfProfile')
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
        name = name.split("-")[0]
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
            item = Prof()
            
            # extract professor name and the link to their profile page 
            name = str(site.select('a/text()').extract())
            if name != "[]":
                firstname, lastname = self.index_prof_name_extract_refine(name)
                print(firstname)
            
            #item['first_name'] = site.select('a/text()').extract()
            #item.save()
            #item['prof_name'] = site.select('a/text()').extract()
            prof_link = site.select('a/@href').extract()
            
            next_page = "http://www.ratemyprofessors.com/" + str(prof_link)[3:-2]            
            if next_page:
                yield Request(next_page, self.parseProfProfile)
            
            #items.append(item)
        filename = "files/" + response.url.split("/")[-1]
        
        
        #open(filename, 'wb').write(response.body)
     
    
    def parseProfProfile(self, response):
        prof_dict = {}
        current_course_dict= {}
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('/html/head/title')
        prof_profile_page_number = "1"
        url = response.url
        path = "//home//draco//Dropbox//SFU//cmpt456//project//cssearchengine//crawler//tutorial//files//"
        first_name =''      # used for djangoitem
        lastname = ''       # used for djangoitem
        name = ''           # used for filename for saving prof profile page
        quality = ''        # used for prof rating scrape from rmp site
        helpfulness = ''    # used for prof rating scrape from rmp site
        easiness = ''       # used for prof rating scrape from rmp site
        clarity = ''        # used for prof rating scrape from rmp site
        
        profList = []       # holds list of prof objects
        class_list = []     # holds list of class objects to store comments and ratings

        if "pageNo" in url:
            prof_profile_page_number = url.split("=")[-1]

        # used to determine if there are multi pages
        flag = False

        # grab prof information and save the page
        # grab prof name below
        for site in sites:
            name = str(site.select('text()').extract())
            firstname, lastname = self.prof_profile_extract_name(name)
            name = firstname + "_" + lastname
        if not os.path.exists(path + name + "//"):
            os.makedirs(path+name+"//")

        # save prof page here    
        #filename = path + name + "//" + name + "_" + prof_profile_page_number
        #open(filename, 'wb').write(response.body)

        # get the score card
        # we only need to parse this once
        if flag == False:
            # get overall quality
            quality = str(hxs.select('//li[@id="quality"]').extract())
            quality = quality.split("strong>")[1][:-2]
            print "Quality: ", quality

            # get helpfulness
            helpfulness = str(hxs.select('//li[@id="helpfulness"]').extract())
            helpfulness = helpfulness.split("strong>")[1][:-2]
            print "helpfulness: ", helpfulness

            # get clarity
            clarity = str(hxs.select('//li[@id="clarity"]').extract())
            clarity = clarity.split("strong>")[1][:-2]
            print "Clarity: ", clarity

            # get easiness
            easiness = str(hxs.select('//li[@id="easiness"]').extract())
            easiness = easiness.split("strong>")[1][:-2]
            print "Easiness: ", easiness

        # we now try to get classes and comments
        # EVEN
        sites = hxs.select('//div[@class="entry even"]')
        
        course_name = ''
        course_easiness = ''
        course_clarity = ''
        course_helpful =''
        
        for site in sites:
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
            rating_dict['easiness'] = course_easiness
            rating_dict['clarity'] = course_clarity
            rating_dict['helpfulness'] = course_helpful
            current_course_dict[course_name] = rating_dict

        #ODD
        sites = hxs.select('//div[@class="entry odd"]')
        for site in sites:
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
            rating_dict['easiness'] = course_easiness
            rating_dict['clarity'] = course_clarity
            rating_dict['helpfulness'] = course_helpful
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
        if prof_profile_page_number != "1":
            print "\n\n", prof_dict
        with open('data.json', 'a') as outfile:
                json.dump(prof_dict, outfile, indent=4)
        outfile.close()
        
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



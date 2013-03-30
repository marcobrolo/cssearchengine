from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from tutorial.items import DmozItem
from tutorial.items import RateMyProfItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http.request import Request
import os


class DmozSpider(BaseSpider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
       # filename = response.url.split("/")[-2]
       # open(filename, 'wb').write(response.body)
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//ul/li')
        items = []
        for site in sites:
            item = DmozItem()
            item['title'] = site.select('a/text()').extract()
            item['link']  = site.select('a/@href').extract()
            item['desc'] = site.select('text()').extract()
            items.append(item)
        return items

class RMPSpider(BaseSpider):
    name = "ratemyprof"
    allowed_domains = ["ratemyprofessors.com"]
    start_urls = [
        "http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=Computer+Science&orderby=TLName&sid=1482",
        "http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=Computer+Science&orderby=TLName&sid=1482&pageNo=2",
        "http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=Computer+Science&orderby=TLName&sid=1482&pageNo=3",
        "http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=Computer+Science&orderby=TLName&sid=1482&pageNo=4",
        "http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=Computer+Science&orderby=TLName&sid=1482&pageNo=5",
        "http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=Computer+Science&orderby=TLName&sid=1482&pageNo=6"
    ]
    rules = [
        Rule(SgmlLinkExtractor()),
        #Rule(SgmlLinkExtractor(allow=[r'SelectTeacher\.jsp\?the_dept=Computer\+Science&orderby=TLName&sid=1482&pageNo=\d+']), follow= True), 
        #Rule(SgmlLinkExtractor(allow=[r'\ShowRatings\\.jsp\\?tid=\d+']), callback = 'parseProfProfile')
    ]
 
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[@class="profName"]')
        items = []
        for site in sites:
            item = RateMyProfItem()
            
            # extract professor name and the link to their profile page 
            item['prof_name'] = site.select('a/text()').extract()
            item['prof_link'] = site.select('a/@href').extract()
            
            next_page = "http://www.ratemyprofessors.com/" + str(item['prof_link'])[3:-2]            
            if next_page:
                yield Request(next_page, self.parseProfProfile)
            
            items.append(item)
        filename = "files/" + response.url.split("/")[-1]
        open(filename, 'wb').write(response.body)
     
    
    def parseProfProfile(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('/html/head/title')
        prof_profile_page_number = "1"
        url = response.url
        path = "//home//draco//Dropbox//SFU//cmpt456//project//cssearchengine//crawler//tutorial//files//"
        if "pageNo" in url:
            prof_profile_page_number = url.split("=")[-1]

        flag = False
        for site in sites:
            name = str(site.select('text()').extract())
            name = name.split("-")[0]
            if "\\xa0" in name:
                name = name[3:]
                if " " in name:
                    name = name.replace(" ","")
                name = name.replace("\\xa0", "_")
        if not os.path.exists(path + name + "//"):
            os.makedirs(path+name+"//")

        filename = path + name + "//" + name + "_" + prof_profile_page_number
        open(filename, 'wb').write(response.body)
        
# Figure out if prof has next page
        sites = hxs.select('//a[@class="next"]')
        for site in sites:
            flag = True
            next_page_url = site.extract().encode('ascii', 'ignore')
            next_page_url = str(next_page_url).split(" ")[1][6:-1]
            next_page_url = next_page_url.replace("&amp;","&")
            next_page_url = "http://www.ratemyprofessors.com" + next_page_url                 
        if flag == True:
            print(name + " has a next page")
            yield Request(next_page_url, self.parseProfProfile)
        else:
            print(name + " does not have a next page")

    def save_content(self, response):
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)

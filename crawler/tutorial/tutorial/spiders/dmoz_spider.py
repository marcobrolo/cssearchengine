from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from tutorial.items import DmozItem

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
    
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[@class="profName"]')
        for site in sites:
            prof_name = site.select('a/text()').extract()
            prof_link = site.select('a/@href').extract()
            print(prof_name, prof_link)

